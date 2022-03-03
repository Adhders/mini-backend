import json
import logging
import re
import jwt
from datetime import datetime, timedelta, timezone
from random import randint

from django import http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from celery_tasks.email.tasks import send_verify_email
from celery_tasks.sms.tasks import send_sms_code
from utils import constants, tools
from utils.response_code import RETCODE
from .models import User

from .utils import generate_verify_email_url, check_verify_email_token

logger = logging.getLogger("django")


class SMSCodesView(View):
    # 短信验证码
    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: 响应结果
        """
        # 发短信之前先判断此手机号是否有没有在60秒内发送过
        # 创建redis连接对象
        redis_conn = get_redis_connection("verify_code")
        # 尝试去获取此手机发送过短信的标记
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        # 如果有，提前响应
        if send_flag:
            return http.JsonResponse({
                "code": RETCODE.THROTTLINGERR,
                "errmsg": "短信发送过于频繁"
            })
        # 图形验证码对比正确，生成6位数短信验证码
        sms_code = "%06d" % randint(0, 999999)
        logger.info(sms_code)

        # 保存短信验证码
        # 创建redis管道
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 向redis中多存储一个此手机号已发送过短信验证码的标记，此标记有效时间60秒
        pl.setex("send_flag_%s" % mobile, constants.SMS_CODE_SEND_FLAG, 1)
        # 执行管道
        pl.execute()
        # Celery异步发送短信验证码
        send_sms_code.delay(mobile, sms_code)
        # 响应结果
        return http.JsonResponse({"code": RETCODE.OK, "errmsg": "短信发送成功"})


class RegisterView(View):
    """用户注册"""

    def post(self, request):
        """
        用户注册实现
        :param request:
        :return:
        """
        # 1.接受参数
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        sms_code = request.POST.get("sms_code")
        # 短信验证码
        # 2.6.1 创建redis连接对象
        redis_conn = get_redis_connection("verify_code")
        # 2.6.2 获取redis中短信验证码
        sms_code_server = redis_conn.get("sms_%s" % mobile)

        # 2.6.3 判断短信验证码是否过期
        if sms_code_server is None:
            return http.JsonResponse({
                "code": RETCODE.SMSCODERR,
                "errmsg": "短信验证码已过期"
            })
        # 2.6.4 如果短信验证码存在，删除redis中存储的短信验证码【目的：一个短信验证码只能使用一次】
        # redis_conn.delete("sms_%s" % mobile)
        # 2.6.5 redis短信验证码由bytes转为字符串类型
        sms_code_server = sms_code_server.decode()

        # 2.6.6 对比短信验证码
        if sms_code_server != sms_code:
            return http.JsonResponse({
                "code": RETCODE.SMSCODERR,
                "errmsg": "请输入正确的短信验证码"
            })
        # 3.业务处理
        # 1.创建用户对象
        try:
            pid = str(int(datetime.now().strftime('%Y'))-2020) + datetime.now().strftime('%m%d%H%M%S')
            user = User(mobile=mobile, pid=pid)
            user.set_password(password)
            user.save()
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})


class LoginView(View):
    """用户登录"""
    def post(self, request, mode):
        """
         实现登录页面逻辑
         :param request:请求对象
         :return: 重定向过来页面
         """
        # 1.接收前段传来的数据
        mobile = request.POST.get('mobile')
        expireDays = request.POST.get('expireDays')
        # 2.1 登录认证
        try:
            # 密码登录
            if mode == 'password':
                password = request.POST.get('password')
                user = authenticate(request, mobile=mobile, password=password)

                if user is None:
                    return http.JsonResponse({
                        'code': RETCODE.PWDERR,
                        "errmsg": "密码错误"
                    })
            # 验证码登录
            else:
                sms_code = request.POST.get('sms_code')
                user = User.objects.get(mobile=mobile)
                redis_conn = get_redis_connection("verify_code")
                # 2.6.2 获取redis中短信验证码
                sms_code_server = redis_conn.get("sms_%s" % mobile)
                # 2.6.3 判断短信验证码是否过期
                if sms_code_server is None:
                    return http.JsonResponse({
                        'code': RETCODE.SMSCODERR,
                        "errmsg": "短信验证码已过期"
                    })
                # 2.6.4 如果短信验证码存在，删除redis中存储的短信验证码【目的：一个短信验证码只能使用一次】
                # redis_conn.delete("sms_%s" % mobile)
                # 2.6.5 redis短信验证码由bytes转为字符串类型
                sms_code_server = sms_code_server.decode()

                # 2.6.6 对比短信验证码
                if sms_code_server != sms_code:
                    return http.JsonResponse({
                        "code": RETCODE.SMSCODERR,
                        "errmsg": "请输入正确的短信验证码"
                    })
            # 2.2 如果if成立,说明用户登录失败
        except Exception:
            return http.HttpResponseForbidden()

        payload = {
            'exp': datetime.now(tz=timezone.utc) + timedelta(days=int(expireDays)),  # 令牌过期时间
            # 'pid': user.pid
        }
        key = 'SECRET_KEY_mini'
        token = jwt.encode(payload, key, algorithm='HS256')

        # 4.响应登录结果
        return http.JsonResponse({"code": RETCODE.OK, 'pid': user.pid, 'token': token})


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """
        实现退出登录逻辑
        :param request: 请求对象
        :return: 响应结果
        """
        # 清理session
        logout(request)
        # 退出登录，重定向回登录页
        response = redirect(reverse('users:login'))
        # 退出登录时清除
        response.delete_cookie('username')

        return response


class MobileCountView(View):

    def get(self, request, mobile):
        """
        手机号重复注册校验
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        try:
            # 使用username查询user表, 得到mobile的数量
            count = User.objects.filter(mobile=mobile).count()
        except Exception:
            return http.HttpResponseForbidden()
        # 响应
        return http.JsonResponse({
            "code": RETCODE.OK,
            "count": count,
        })


class ChangePasswordView(RegisterView):
    """修改密码"""
    pass


class LoginRequiredView(LoginRequiredMixin, View):
    """自定义一个登录判断类"""
    pass


class EmailView(LoginRequiredView):
    """添加邮箱"""

    def put(self, request):
        # 接收参数
        json_dict = json.loads(request.body)
        email = json_dict.get('email')

        # 校验参数
        if not email:
            return http.JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '缺少email参数'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.JsonResponse({'code': RETCODE.EMAILERR, 'errmsg': '邮箱格式错误'})

        # 业务逻辑处理
        # 获取登录用户
        user = request.user
        # 修改email
        User.objects.filter(username=User.username, email='').update(email=email)

        # 发送邮件
        try:
            # 给当前登录用户的模型对象user的email字段赋值
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})

        # 异步发送验证邮件
        # 生成邮箱激活链接
        verify_url = generate_verify_email_url(user)
        # celery进行异步发送邮件
        send_verify_email.delay(email, verify_url)

        # 响应添加邮箱结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})


class VerifyEmailView(LoginRequiredView):
    """验证邮件"""

    def get(self, request):
        # 获取数据
        token = request.GET.get('token')

        # 校验参数，判断token是否为空或过期，提前user
        if token is None:
            return http.HttpResponseBadRequest('缺少token')

        user = check_verify_email_token(token)
        if user is None:
            return http.HttpResponseForbidden('无效的token')

        # 修改email_active的值为True
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮件失败')

        # 响应：返回激活邮件结果
        return redirect(reverse('users:info'))

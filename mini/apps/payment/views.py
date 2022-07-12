from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import json
import string
import random
import time
import logging
from django import http
from django.views import View
from orders.models import RefundOrder, Order
from orders.views import OrdersView
from store.models import Store
from utils.response_code import RETCODE
import xml.etree.ElementTree as et
from django.utils import timezone
from wechatpayv3 import SignType, WeChatPay, WeChatPayType

# # 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
# MCHID = '1618935182'
#
# # 商户证书私钥
# with open('path_to_key/apiclient_key.pem') as f:
#     PRIVATE_KEY = f.read()

# # 商户证书序列号
# CERT_SERIAL_NO = '5F9DF80CE5F4D8311A0720A6712BE628E7D60345'
#
# # API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
# APIV3_KEY = 'communistentrepreneurlijunbo1991'
#
# # APPID，应用ID或服务商模式下的sp_appid
# APPID = 'wx09760711e33ab5bb'

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'http://localhost:8000/notify'

# 微信支付平台证书缓存目录，减少证书下载调用次数
# 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
CERT_DIR = None

LOGGER = logging.getLogger("django")

# # 接入模式:False=直连商户模式，True=服务商模式
# PARTNER_MODE = False

# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None


def payback(request):
    _xml = request.body
    # 拿到微信发送的xml请求 即微信支付后的回调内容
    xml = str(_xml, encoding="utf-8")
    return_dict = {}
    tree = et.fromstring(xml)
    # xml 解析
    return_code = tree.find("return_code").text
    try:
        if return_code == 'FAIL':
            # 官方发出错误
            return_dict['message'] = '支付失败'
            # return Response(return_dict, status=status.HTTP_400_BAD_REQUEST)
        elif return_code == 'SUCCESS':
            # 拿到自己这次支付的 out_trade_no
            _out_trade_no = tree.find("out_trade_no").text
            # 这里省略了 拿到订单号后的操作 看自己的业务需求
    except Exception as e:
        pass
    finally:
        return HttpResponse(return_dict, status='200')


def getwepay(APPID, WECHATPAY_TYPE, MCHID, CERT_SERIAL_NO, APIV3_KEY, PARTNER_MODE, CERT_PATH):
    with open(CERT_PATH) as f:
        PRIVATE_KEY = f.read()
    res = WeChatPay(
        wechatpay_type=WECHATPAY_TYPE,
        mchid=MCHID,
        private_key=PRIVATE_KEY,
        cert_serial_no=CERT_SERIAL_NO,
        apiv3_key=APIV3_KEY,
        appid=APPID,
        notify_url=NOTIFY_URL,
        cert_dir=CERT_DIR,
        logger=LOGGER,
        partner_mode=PARTNER_MODE,
        proxy=PROXY)
    return res


# class NativePay(View):
#     def post(self, request):
#         # 以native下单为例，下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试。
#         out_trade_no = ''.join(sample(ascii_letters + digits, 8))
#         description = 'demo-description'
#         amount = 1
#         try:
#             wxpay = getwepay(WeChatPayType.NATIVE)
#             code, message = wxpay.pay(
#                 description=description,
#                 out_trade_no=out_trade_no,
#                 amount={'total': amount}
#             )
#         except Exception as e:
#             return http.HttpResponseForbidden()
#             # 4.响应
#         return http.JsonResponse({"code": code, 'message': message})


class MiniProgPay(View):
    def post(self, request, appid, pid):
        # 小程序支付下单，wxpay初始化的时候，wechatpay_type设置为WeChatPayType.MINIPROG。
        # 下单成功后，将prepay_id和其他必须的参数组合传递给小程序的wx.requestPayment接口唤起支付
        try:
            store = Store.objects.get(appid=appid)
            store_setting = store.store_setting
            if store_setting.exists():
                paymentSetting = store_setting.first().paymentSetting['wechat_mini_prog']
            else:
                return http.HttpResponseForbidden()
            order = OrdersView.post(request, appid, pid)
            description = order['description']
            out_trade_no = order['orderNum']
            payer = {'openid': order['openid']}
            total = order['total']
            wxpay = getwepay(
                appid,
                WeChatPayType.MINIPROG,
                paymentSetting['mchid'],
                paymentSetting['cert_serial_no'],
                paymentSetting['apiv3_key'],
                paymentSetting['partner_mode'],
                paymentSetting['cert']
            )
            code, message = wxpay.pay(
                description=description,
                out_trade_no=out_trade_no,
                amount={'total': int(total)},
                payer=payer
            )
            # print(code, message, total)
            result = json.loads(message)
            if code in range(200, 300):
                prepay_id = result.get('prepay_id')
                timestamp = str(int(time.time()))
                noncestr = ''.join(random.sample(string.ascii_letters + string.digits, 32))  # 随机字符串不超过32位
                package = 'prepay_id=' + prepay_id
                paysign = wxpay.sign(data=[appid, timestamp, noncestr, package], sign_type=SignType.RSA_SHA256)
                signtype = 'RSA'
                return http.JsonResponse({'code': RETCODE.OK, 'result': {
                    'appId': appid,
                    'timeStamp': timestamp,
                    'nonceStr': noncestr,
                    'package': 'prepay_id=%s' % prepay_id,
                    'signType': signtype,
                    'paySign': paysign
                }, 'orderNum': out_trade_no})
            else:
                return http.JsonResponse({'code': -1, 'result': {'reason': result.get('code')}})
        except Exception as e:
            LOGGER.error(e)
            return http.HttpResponseForbidden()

    def get(self, request, appid, orderNum):
        store = Store.objects.get(appid=appid)
        store_setting = store.store_setting
        if store_setting.exists():
            paymentSetting = store_setting.first().paymentSetting['wechat_mini_prog']
        else:
            return http.HttpResponseForbidden()
        wxpay = getwepay(
            appid,
            WeChatPayType.MINIPROG,
            paymentSetting['mchid'],
            paymentSetting['cert_serial_no'],
            paymentSetting['apiv3_key'],
            paymentSetting['partner_mode'],
            paymentSetting['cert']
        )
        code, message = wxpay.query(out_trade_no=orderNum)
        return http.JsonResponse({'code': RETCODE.OK, 'message': message})


class MiniProgRefound(View):
    def post(self, request, pid, store_id):
        data = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store_setting = store.store_setting
            if store_setting.exists():
                paymentSetting = store_setting.first().paymentSetting['wechat_mini_prog']
            else:
                return http.HttpResponseForbidden()
            appid = store.appid
            wxpay = getwepay(
                appid,
                WeChatPayType.MINIPROG,
                paymentSetting['mchid'],
                paymentSetting['cert_serial_no'],
                paymentSetting['apiv3_key'],
                paymentSetting['partner_mode'],
                paymentSetting['cert']
            )
            code, message = wxpay.refund(
                out_refund_no=data['refundNum'],
                amount=data['amount'],
                out_trade_no=data['orderNum']
            )
            if code == 200:
                RefundOrder.objects.filter(refundNum=data['refundNum']).update(status="退款成功",
                                                                               refund_time=timezone.now())
        except Exception as e:
            LOGGER.error(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': code, 'message': message})


class MiniProgClose(View):
    def get(self, request, appid, orderNum):
        try:
            store = Store.objects.get(appid=appid)
            store_setting = store.store_setting
            if store_setting.exists():
                paymentSetting = store_setting.first().paymentSetting['wechat_mini_prog']
            else:
                return http.HttpResponseForbidden()
            wxpay = getwepay(
                appid,
                WeChatPayType.MINIPROG,
                paymentSetting['mchid'],
                paymentSetting['cert_serial_no'],
                paymentSetting['apiv3_key'],
                paymentSetting['partner_mode'],
                paymentSetting['cert']
            )
            code, message = wxpay.close(
                out_trade_no=orderNum
            )
            if code == 204:
                Order.objects.filter(orderNum=orderNum).update(status="交易关闭")
            if code == 400:
                Order.objects.filter(orderNum=orderNum).update(status="待评价", payment_time=timezone.now())
        except Exception as e:
            LOGGER.error(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': code, "message": message})

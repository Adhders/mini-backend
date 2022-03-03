from django.shortcuts import render

# Create your views here.
import json
import string
import random
import time
import logging
from django import http
from django.views import View
from orders.views import OrdersView
from utils.response_code import RETCODE
from random import sample
from string import ascii_letters, digits
from wechatpayv3 import SignType, WeChatPay, WeChatPayType
from datetime import datetime, timedelta, timezone

# 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
MCHID = '1618935182'

# 商户证书私钥
with open('path_to_key/apiclient_key.pem') as f:
    PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '5F9DF80CE5F4D8311A0720A6712BE628E7D60345'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'communistentrepreneurlijunbo1991'

# APPID，应用ID或服务商模式下的sp_appid
APPID = 'wx09760711e33ab5bb'

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'http://127.0.0.1:5000/notify'

# 微信支付平台证书缓存目录，减少证书下载调用次数
# 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
CERT_DIR = None

LOGGER = logging.getLogger("django")

# 接入模式:False=直连商户模式，True=服务商模式
PARTNER_MODE = False

# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None


def getwepay(wechatpay_type):
    res = WeChatPay(
        wechatpay_type=wechatpay_type,
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


class NativePay(View):
    def post(self, request):
        # 以native下单为例，下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试。
        out_trade_no = ''.join(sample(ascii_letters + digits, 8))
        description = 'demo-description'
        amount = 1
        try:
            wxpay = getwepay(WeChatPayType.NATIVE)
            code, message = wxpay.pay(
                description=description,
                out_trade_no=out_trade_no,
                amount={'total': amount}
            )
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
            # 4.响应
        return http.JsonResponse({"code": code, 'message': message})


class MiniProgPay(View):
    def post(self, request, appid, pid):
        # 小程序支付下单，wxpay初始化的时候，wechatpay_type设置为WeChatPayType.MINIPROG。
        # 下单成功后，将prepay_id和其他必须的参数组合传递给小程序的wx.requestPayment接口唤起支付
        try:
            res = OrdersView.post(request, appid, pid)
            print('res', res)
            description = res['description']
            out_trade_no = res['orderNum']
            payer = {'openid': res['openid']}
            wxpay = getwepay(WeChatPayType.MINIPROG)
            code, message = wxpay.pay(
                description=description,
                out_trade_no=out_trade_no,
                amount={'total': 1},
                payer=payer
            )
            result = json.loads(message)
            if code in range(200, 300):
                print('code', code)
                prepay_id = result.get('prepay_id')
                timestamp = str(int(time.time()))
                noncestr = ''.join(random.sample(string.ascii_letters + string.digits, 32)) #随机字符串不超过32位
                package = 'prepay_id=' + prepay_id
                paysign = wxpay.sign(data=[APPID, timestamp, noncestr, package], sign_type=SignType.RSA_SHA256)
                signtype = 'RSA'
                return http.JsonResponse({'code': RETCODE.OK, 'result': {
                    'appId': APPID,
                    'timeStamp': timestamp,
                    'nonceStr': noncestr,
                    'package': 'prepay_id=%s' % prepay_id,
                    'signType': signtype,
                    'paySign': paysign
                }, 'orderNum': res['orderNum']})
            else:
                return http.JsonResponse({'code': -1, 'result': {'reason': result.get('code')}})
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()

    def get(self, request, orderNum):
        wxpay = getwepay(WeChatPayType.MINIPROG)
        code, message = wxpay.query(out_trade_no=orderNum)
        print('code: %s, message: %s' % (code, message))
        return http.JsonResponse({'code': RETCODE.OK})


class MiniProgRefound(View):
    def post(self, request, orderNum):
        wxpay = getwepay(WeChatPayType.MINIPROG)
        code, message = wxpay.refund(
            out_refund_no=orderNum,
            amount={'refund': 100, 'total': 100, 'currency': 'CNY'},
            out_trade_no=orderNum
        )
        print('code: %s, message: %s' % (code, message))
        return http.JsonResponse({'code': code})


class MiniProgClose(View):
    def get(self, request, orderNum):
        try:
            wxpay = getwepay(WeChatPayType.MINIPROG)
            code, message = wxpay.close(
                out_trade_no=orderNum
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': code})

# -*- coding:utf-8 -*-

from ronglian_sms_sdk import SmsSDK
import json
# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8a216da87a332d53017ab38feb532a44'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = '87b2ce87675748c0aa9dbfc803cc4aca'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8a216da87a332d53017ab38fec462a4a'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'
# _serverIP = 'app.cloopen.com'


class CCP(object):
    """发送短信的辅助类"""

    def __new__(cls, *args, **kwargs):
        # 判断是否存在类属性_instance，_instance是类CCP的唯一对象，即单例
        if not hasattr(CCP, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls._instance.rest = SmsSDK(_accountSid, _accountToken , _appId)
        return cls._instance

    def send_template_sms(self,temp_id, to, datas):
        """发送模板短信"""
        # @param to 手机号码
        # @param datas 内容数据 格式为数组 例如：['短信验证码','提示的过期时间分钟']，如不需替换请填 ''
        # @param temp_id 模板Id
        result = json.loads(self.rest.sendMessage(temp_id,to, datas))
        print(result)
        # 如果云通讯发送短信成功，返回的字典数据result中statuCode字段的值为"000000"
        if result.get("statusCode") == "000000":
            # 返回0 表示发送短信成功
            return 0
        else:
            # 返回-1 表示发送失败
            return -1

if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1
    res=CCP().send_template_sms(1,'13661451627', ['1234', 5])
    print(res)


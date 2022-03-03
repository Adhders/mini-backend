from ronglian_sms_sdk import SmsSDK

accId = '8a216da87a332d53017ab38feb532a44'
accToken = '87b2ce87675748c0aa9dbfc803cc4aca'
appId = '8a216da87a332d53017ab38fec462a4a'

def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    tid = "1"
    mobile = '15639525339'
    datas = ('变量1', '变量2')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)

send_message()

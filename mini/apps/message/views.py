from django.shortcuts import render

# Create your views here.
import time
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket

#
# @accept_websocket
# def test(request):
#     if request.is_websocket():
#         print('websocket connection....')
#         msg = request.websocket.wait()  # 接收前端发来的消息
#         print(msg, type(msg), json.loads(msg))  # b'["1","2","3"]' <class 'bytes'> ['1', '2', '3']
#         while 1:
#             if msg:
#                 # 你要返回的结果
#                 for i in range(10):
#                     request.websocket.send('service message: {}'.format(i).encode())  # 向客户端发送数据
#                     time.sleep(0.5)  # 每0.5秒发一次
#                 request.websocket.close()
#     else:  # 如果是普通的请求返回页面
#         return render(request, 'test.html')


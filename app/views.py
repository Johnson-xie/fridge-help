import uuid

from django.shortcuts import render, HttpResponse  # 引入HttpResponse
from dwebsocket.decorators import accept_websocket  # 引入dwbsocket的accept_websocket装饰器


def to_sendmsg(request):
    return render(request, 'sendmsg.html')


def to_recmsg(request):
    return render(request, 'recmsg.html')


clients={} #创建客户端列表，存储所有在线客户端


# 允许接受ws请求
@accept_websocket
def link(request):
    # 判断是不是ws请求
    if request.is_websocket():
        userid = str(uuid.uuid1())
        # 判断是否有客户端发来消息，若有则进行处理，若发来“test”表示客户端与服务器建立链接成功
        while True:
            message = request.websocket.wait()
            if not message:
                break
            else:
                print("客户端链接成功：" + str(message, encoding="utf-8"))
                # 保存客户端的ws对象，以便给客户端发送消息,每个客户端分配一个唯一标识
                clients[userid] = request.websocket


def send(request):
    # 获取消息
    msg=request.POST.get("msg")
    # 获取到当前所有在线客户端，即clients
    # 遍历给所有客户端推送消息
    for client in clients:
        clients[client].send(msg.encode('utf-8'))
    return HttpResponse({"msg": "success"})
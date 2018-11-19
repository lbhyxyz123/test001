import socket
import re
import gevent
import sys
from gevent import monkey
monkey.patch_all()
import Application


class HttpServer(object):
    #初始化套接字
    def __init__(self,port):
        # 创建套接字,设置端口重用,绑定端口,设置监听
        tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        tcp_server_socket.bind(('',port))
        tcp_server_socket.listen(5)
        # 套接字保存实例属性中
        self.tcp_server_socket = tcp_server_socket

    def start(self):
        # 等待客户端连接,能够接收多个客户端连接
        while True:
            new_client_socket ,ip_port = self.tcp_server_socket.accept()
            print('新客户来啦:',ip_port)
            # request_handler(new_client_socket)
            g1 = gevent.spawn(self.request_handler,new_client_socket )
            # 因为接收客户端连接的是死循环,主线程不会退出,协程会执行完
            # g1.join()

    def request_handler(self,new_client_socket):
        # 接收浏览器请求,并判断是否为空
        recv_data = new_client_socket.recv(1024)
        if not recv_data:
            print('浏览器可能已经关闭')
            new_client_socket.close()
            return

        # 收到内容解码
        request_text = recv_data.decode()
        # 根据\r\n拆分字符串,得到第一行
        request_list = request_text.split('\r\n')
        # request_list[0] 就是请求行
        ret = re.search(r'/.*\s',request_list[0])
        # 判断报文是否有误 not ret 假假得真
        if not ret:
            print('浏览器请求的报文格式错误!')
            new_client_socket.close()
            return
        # 获取路径
        path_info = ret.group()
        print(path_info)
        
        if path_info == "/":
            print(1111)
            path_info = "/index.html"
        
        print(path_info)

        # 拼接响应报文 判断如果是动态资源交给框架处理
        if path_info.endswith('.html'):
            # 字典存储用户的请求信息
            env = { 'PATH_INFO':path_info}
            # 调用框架
            status ,headers,response_body = Application.app(env)
            # 用框架返回的数据拼接报文
            response_line = 'HTTP/1.1 %s\r\n' %status

            response_header = ''
            for header in headers: # 元组拿出来拆包放 : 两边
                response_header += '%s:%s\r\n'%header

            response_data = response_line + response_header + '\r\n' + response_body
            new_clinet_socket.send(response_data.encode())
            new_client_socket.close()
        # 如果不是/html 则认为是静态资源
        else:
            response_header = 'Server:PythonWS1.0\r\n'
            response_blank = '\r\n'
            # response_content = 'Hello world!\r\n'
            # print("static"+path_info+"//////1111111111111111111")
            lujin = "static1"+path_info
            print(lujin)
            try:
                with open(lujin,'rb') as file:
                    response_content = file.read()
                    
            except Exception as e:
                response_line = 'HTTP/1.1 404 Not Found\r\n'
                response_content = 'Error! %s'%str(e)
                # 对返回的内容进行编码
                response_content = response_content.encode()
            else:
                response_line = 'HTTP/1.1 200 OK\r\n'
            finally:
                # 定义变量保存响应报文内容
                response_data = (response_line + response_header + response_blank).encode() + response_content
                # 发送响应报文给客户端
                new_client_socket.send(response_data)
                # 关闭此次套接字
                new_client_socket.close()



def main():
    #sys.argv 可以获取终端启动程序时的启动参数,并返回一改列表,列表依次保存我们输入的参数内容
    #print(sys.argv)

    if len(sys.argv) != 2:
        print('服务器启动失败,输入格式: python3 HttpServer.py port')
        return
    # 判断端口号,是不是一改纯数字
    if not sys.argv[1].isdigit():
        print('服务器启动失败,端口号应该是纯数字!')
        return

    # 获取端口号
    port = int(sys.argv[1])
    # 实例化 HttpServer(port)
    httpserver = HttpServer(port)
    # 启动服务器
    httpserver.start()


if __name__ == '__main__':
    main()

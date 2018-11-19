"""web 框架 web应用 """
import time

def get_time():
    """ 当用户请求/gettime.html 执行当前方法 """
    return time.ctime()

def app(env):
    # 接收 取出用户信息
    path_info = env["PATH_INFO"]
    prinit("接收到用户的动态资源请求%s"%path_info)
    # 数据库 等处理
    if path_info == '/gettime.html':
        # 状态 响应头 响应体
        return '200 OK',[('server','XIVI1.0')],get_time()
    else:
        # 状态 响应头 响应体
        return '404 Not Found',[('Server','XIVI1.0')],'response body from app'

import ssl
import socket


def parsed_url(url):
    """
    解析 url 返回 (protocol host port path)
    有的时候有的函数, 它本身就美不起来, 你要做的就是老老实实写
    http://www.zhihu.com:80/question/31838184?xxx=yyy
    """
    # 检查协议
    # '://' 定位 然后取第一个 / 的位置来切片
    separator = '://'
    i = url.find(separator)
    if i == -1:
        protocol = 'http'
        u = url
    else:
        protocol = url[:i]
        u = url[i + len(separator):]
    print('protocol and u', protocol, u)

    # 检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    i = host.find(':')
    if i == -1:
        # 检查端口
        # 表驱动法
        port_dict = {
            'http': 80,
            'https': 443,
        }
        # 默认端口
        port = port_dict[protocol]
        # if protocol == 'http':
        #     port = 80
        # elif protocol == 'https':
        #     port = 443
        # else
        #   error
        #
        # if protocol == 'http':
        #     port = 80
        # else:
        #     port = 443
    else:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def parsed_response(r):
    """
    解析出 状态码 headers body

    HTTP/1.1 301 Moved Permanently
    Date: Wed, 16 May 2018 12:27:49 GMT
    Content-Type: text/html
    Transfer-Encoding: chunked
    Connection: keep-alive
    Keep-Alive: timeout=30
    Location: https://movie.douban.com/top250
    Server: dae
    X-Content-Type-Options: nosniff

    b2
    <html>

    """
    # 只 split 一下，因为 body 可能包含换行符
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v

    return status_code, headers, body


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        print('new loop')
        r = s.recv(buffer_size)
        print('response', len(r), r)
        response += r
        if len(r) < buffer_size:
            return response


def socket_by_protocol(protocol):
    s = socket.socket()
    if protocol == 'https':
        return ssl.wrap_socket(s)
    else:
        return s


# 复杂的逻辑全部封装成函数

def get(url):
    """
    用 GET 请求 url 并返回响应
    """
    protocol, host, port, path = parsed_url(url)
    print('log request', protocol, host, port, path)

    s = socket_by_protocol(protocol)
    s.connect((host, port))

    # Connection 有两个选项 close 和 keep-alive
    # 要么就一次 recv 所有数据
    # 要么就用无限循环加 Connection: close
    # '' % path
    request = 'GET {} HTTP/1.1\r\nHost: {}\r\nCookie: session_id=kjjjklkkkljjkkjk\r\n\r\n'.format(path, host)
    # encode 的 'utf-8' 参数可以省略
    s.send(request.encode())

    response = response_by_socket(s)
    r = response.decode()
    print('response:\n', r)
    status_code, headers, body = parsed_response(r)

    if status_code == 301:
        url = headers['Location']
        return get(url)
    else:
        return response, status_code


def main():
    # url = 'http://movie.douban.com/top250'
    url = 'http://localhost:3000/login'
    response, status_code = get(url)
    # decode 的 'utf-8' 参数可以省略
    print(response.decode())


# 以下 test 开头的函数是单元测试
def test_parsed_url():
    """
    parsed_url 函数很容易出错,
    所以我们写测试函数来运行看检测是否正确运行
    """
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        #
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        # assert 是一个语句, 名字叫 断言
        # 如果断言成功, 条件成立,
        # 则通过测试, 否则为测试失败, 中断程序报错
        e = "parsed_url ERROR, ({}) ({}) ({})".format(
            url, u, expected
        )
        # assert 1==2, '1 is not equal to 2'
        assert u == expected, e


def test_get():
    """
    测试是否能正确处理请求
    """
    url = 'http://movie.douban.com/top250'
    response, status_code = get(url)
    expected = 200
    e = "get ERROR, ({}) ({}) ({}) ({})".format(
        url, response, status_code, expected
    )
    assert expected == status_code, e


def test():
    """
    用于测试的主函数
    """
    test_parsed_url()
    test_get()


if __name__ == '__main__':
    # test()
    main()


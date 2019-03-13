from utils import log
from models.message import Message
from models.user import User
from models.session import Session

import random

session_date = {}


def random_string():
    seed = 'kjlkjlkjlkljlkjkl'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s



def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def error(request, code=404):
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def current_user(request):
    # username = request.cookies.get('user', User.guest())
    log('这是cookie', request.cookies)
    session_id = request.cookies.get('session_id', '')
    log('这是session_id', session_id)
    s = Session.find_by(session_id='{}'.format(session_id))
    # username = Session.find_by(session_id='{}'.format(session_id)).get(session_id, User.guest())
    log('这是查找到的s', s)
    if s:
        return s.username
    else:
        return User.guest()
    # return username


def response_with_headers(headers):
    header = 'HTTP/1.x 210 VERY OK\r\n'
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def route_index(request):
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body
    return r.encode()


def route_login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    log('login, headers', request.headers)
    log('login, cookies', request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            session_id = random_string()
            session_date['username'] = u.username
            session_date['session_id'] = session_id
            log('这个才是session', session_date)
            s = Session.new(session_date)
            s.save()
            headers['Set-Cookie'] = 'session_id={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''

    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = '{}\r\n{}'.format(header, body)
    log('login 的响应', r)
    return r.encode()


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode()


def route_message(request):
    username = current_user(request)
    # if username == '【游客】':
    if username == User.guest():
        return error(request)
    else:
        log('本次请求的 method', request.method)
        if request.method == 'POST':
            data = request.form()
        else:
            data = request.query

        if len(data) > 0:
            log('post', data)
            m = Message.new(data)
            m.save()

        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = template('messages.html')
        ms = '<br>'.join([str(m) for m in Message.all()])
        body = body.replace('{{messages}}', ms)
        r = header + '\r\n' + body
        return r.encode()


def route_static(request):
    filename = request.query['file']
    path = 'static/{}'.format(filename)
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        r = header + b'\r\n' + f.read()
        return r

def route_profile(request):
    username = current_user(request)
    if username == User.guest():
        log('进来了')
        header = 'HTTP/1.1 302 OK\r\nContent-Type: text/html\r\nLocation: http://localhost:3000/login\r\n'
        body = '\r\n\r\n'
        r = header + '\r\n' + body
        return r.encode()
    else:
        log('进来二')
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = template('profile.html')
        u = User.find_by(username='{}'.format(username))
        id = str(u.id)
        note = u.note
        body = body.replace('{{id}}', id)
        body = body.replace('{{username}}', username)
        body = body.replace('{{note}}', note)
        r = header + '\r\n' + body
        return r.encode()


def route_dict():
    d = {
        '/': route_index,
        '/static': route_static,
        '/login': route_login,
        '/register': route_register,
        '/messages': route_message,
        '/profile': route_profile,
    }
    return d

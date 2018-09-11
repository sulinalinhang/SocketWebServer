from models import Model


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    @staticmethod
    def guest():
        return '【游客】'

    def validate_login(self):
        # for 循环版本
        # us = User.all()
        # for u in us:
        #     if u.username == self.username and u.password == self.password:
        #         return True
        # return False
        # find_by 版本
        u = User.find_by(username=self.username, password=self.password)
        return u is not None
        # if 0
        # if a == 0
        # if None
        # if 1
        # return u is not None and u.password == self.password
        # u = User.find_by(username=self.username)
        # 不应该用下面的隐式转换
        # return u and u.password == self.password


    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

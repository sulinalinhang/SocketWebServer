from models import Model


class User(Model):
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    @staticmethod
    def guest():
        return '【游客】'

    def validate_login(self):
        u = User.find_by(username=self.username, password=self.password)
        return u is not None


    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

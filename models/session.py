from models import Model


class Session(Model):
    """
    Message 是用来保存留言的 model
    """
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.session_id = form.get('session_id', '')
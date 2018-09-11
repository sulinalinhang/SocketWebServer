import json

from utils import log


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


class Model(object):
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """

    def __init__(self, form):
        self.id = form.get('id', None)
        # self.delted = xxx
        # self.id = None

    @classmethod
    def db_path(cls):
        """
        cls 是类名, 谁调用的类名就是谁的
        classmethod 有一个参数是 class(这里我们用 cls 这个名字)
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        # cls(form) 相当于 User(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        log('models in all', models)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls.new(m) 可以初始化一个 cls 的实例
        # 不明白就 log 大法看看这些都是啥
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        log('find_by kwargs', kwargs)

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
                    log('exist', m, k)
            if exist:
                return m
        # return None

    @classmethod
    def find_all(cls, **kwargs):
        log('find_by kwargs', kwargs)
        models = []

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) and not getattr(m, k) == v:
                    exist = False
            if exist:
                models.append(m)

        return models

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """

        models = self.all()
        log('models <{}>'.format(models))

        if self.id is None:
            # 加上 id
            log('id is None', self)
            if len(models) > 0:
                log('不是第一个元素 <{}>'.format(models[-1].id))
                self.id = models[-1].id + 1
            else:
                log('第一个元素')
                self.id = 1
            models.append(self)
        else:
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并替换
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        # 保存
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        不明白就看书或者 搜
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
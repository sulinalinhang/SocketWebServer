from models.user import User


def test_save():
    # 数据清理
    with open(User.db_path(), 'w') as f:
        f.write('[]')

    # 数据准备
    form = dict(
        username='gua',
        password='123',
    )

    # 测试 id 赋值
    for i in range(1, 5):
        form['username'] = 'gua{}'.format(i)
        u = User.new(form)
        u.save()
        assert u.id == i

    # 测试保存的数据
    for i, u in enumerate(User.all()):
        assert u.id == i + 1

if __name__ == '__main__':
    test_save()
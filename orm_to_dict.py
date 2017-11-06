def orm_to_dict(orm, exclude = []):
    """ ORM对象转可序列化字典 """
    if not orm:
        return {}

    tmp = orm.__dict__
    if tmp.get('_sa_instance_state', None):
        del tmp['_sa_instance_state']

    for x, y in tmp.items():
        if x in exclude:
            del tmp[x]
            continue

        if type(y) is Decimal:
            tmp[x] = float(y)
        elif type(y) is datetime:
            tmp[x] = y.strftime('%Y-%m-%d %H:%M:%S')

    return tmp

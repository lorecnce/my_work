def member_post_json_utils(func):
    """ 官方网站最新接受post方法的json数据的通用装饰器 """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get('Content-Type') == 'application/json; charset=utf-8':
            input_data = request.get_data()
            data = json.loads(input_data)
        else:
            data = request.form.to_dict()

        kwargs.update(data)
        return func(*args, **kwargs)

    return wrapper
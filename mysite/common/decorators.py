from django.http import HttpResponseBadRequest


def ajax_required(f):
    """
    装饰器：只允许ajax请求
    :param f: 视图函数
    :return: 视图函数
    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest() # 400
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

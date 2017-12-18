from .cart import Cart


def cart(req):
    """
    购物车上下文处理器，接受request参数，返回对象字典
    使得所有通过RequestContext渲染的模板可以通过cart访问Cart对象
    :param req:
    :return:
    """
    return {'cart': Cart(req)}

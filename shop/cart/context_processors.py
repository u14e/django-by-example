from .cart import Cart


def cart(request):
    return dict(cart=Cart(request))

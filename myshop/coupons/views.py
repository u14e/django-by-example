from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(req):
    now = timezone.now()
    form = CouponApplyForm(req.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,  # 忽略大小写
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            req.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            print('xxxx coupon {} does not exit'.format(code))
            req.session['coupon_id'] = None
    return redirect('cart:cart_detail')


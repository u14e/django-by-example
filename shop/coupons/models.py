from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='优惠码')
    valid_from = models.DateTimeField(verbose_name='有效起始时间')
    valid_to = models.DateTimeField(verbose_name='有效结束时间')
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)],
                                   verbose_name='折扣率')
    active = models.BooleanField()

    def __str__(self):
        return self.code
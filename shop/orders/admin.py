import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    """
    自定义action
    """
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # 第一行写入表头
    writer.writerow([field.verbose_name for field in fields])
    # 后面行写入数据
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d')
            data_row.append(value)
        writer.writerow(data_row)

    return response


export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    """
    自定义字段
    """
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])
    ))


def order_pdf(obj):
    """
    导出pdf
    """
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id])
    ))


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'address', 'postal_code',
                    'city', 'paid', 'created', 'updated',
                    order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]   # 导出csv文件


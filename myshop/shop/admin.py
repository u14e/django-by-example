from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}  # 自动设置slug的值


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'stock', 'updated']
    # 可以直接在list_display页面修改字段
    # 所以list_editable的字段必须包含在list_display字段中
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}  # 自动设置slug的值


admin.site.register(Product, ProductAdmin)

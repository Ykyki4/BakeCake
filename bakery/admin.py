from django.contrib import admin

from .models import Order, OrderCake


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderCake)
class OrderCakeAdmin(admin.ModelAdmin):
    pass
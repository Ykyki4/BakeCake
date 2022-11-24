from django.contrib import admin

from .models import User, Order, OrderCake


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderCake)
class OrderCakeAdmin(admin.ModelAdmin):
    pass
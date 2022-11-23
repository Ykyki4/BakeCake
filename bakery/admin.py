from django.contrib import admin

from .models import User, Order, OrderCake


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
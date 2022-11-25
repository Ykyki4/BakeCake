from django.contrib import admin

from .models import User, Order, OrderCake, Payment


class CakeInline(admin.TabularInline):
    model = Order
    raw_id_fields = ('cake',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderCake)
class OrderCakeAdmin(admin.ModelAdmin):
    inlines = (CakeInline,)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass




from django.contrib import admin

from .models import Order, OrderCake, Payment


class CakeInline(admin.TabularInline):
    model = OrderCake
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', ]
    inlines = [CakeInline, ]


@admin.register(OrderCake)
class OrderCakeAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    raw_id_fields = ['order', ]
    readonly_fields = ['yookassa_payment_id', 'order']

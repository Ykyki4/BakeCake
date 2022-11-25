from django.urls import path

from .views import register_user, register_order


app_name = 'bakery'

urlpatterns = [
    path('user/', register_user, name='user_reg'),
    path('order/', register_order, name='register_order'),
]

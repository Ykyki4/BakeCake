from django.urls import path

from .views import register_user


app_name = 'bakery'

urlpatterns = [
    path('user/', register_user, name='user_reg')
]
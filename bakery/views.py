from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import Serializer, ModelSerializer, CharField, EmailField, DateField, TimeField

from .models import User, Order, OrderCake


class UserSerializer(ModelSerializer):
    NAME = CharField(source='name')
    PHONE = PhoneNumberField(source='phone')
    EMAIL = EmailField(source='email')

    class Meta:
        model = User
        fields = ['NAME', 'PHONE', 'EMAIL']


class OrderSerializer(ModelSerializer):
    ADDRESS = CharField(source='address')
    DATE = DateField(source='date')
    TIME = TimeField(source='time')
    DELIVCOMMENTS = CharField(source='delivcomment', required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = ['ADDRESS', 'DATE', 'TIME', 'DELIVCOMMENTS']


class CakeSerializer(ModelSerializer):
    LEVELS = CharField(source='levels')
    FORM = CharField(source='form')
    TOPPING = CharField(source='topping')
    BERRIES = CharField(source='berries')
    DECOR = CharField(source='decor')
    WORDS = CharField(source='words', required=False, allow_blank=True)
    COMMENT = CharField(source='comment', required=False, allow_blank=True)

    class Meta:
        model = OrderCake
        fields = ['LEVELS', 'FORM', 'TOPPING', 'BERRIES', 'DECOR', 'WORDS', 'COMMENT',]


def register_user(request):
    User.objects.create(phone=request.GET['REG'])
    return redirect('lk')


@api_view(['POST'])
def register_order(request):
    cake_serializer = CakeSerializer(data=request.data)
    cake_serializer.is_valid(raise_exception=True)
    order_serializer = OrderSerializer(data=request.data)
    order_serializer.is_valid(raise_exception=True)
    user_serializer = UserSerializer(data=request.data)
    user_serializer.is_valid()
    return redirect('start_page')
    # return Response()

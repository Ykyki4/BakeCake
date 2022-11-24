from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import Serializer, ModelSerializer, CharField, EmailField, DateField, TimeField

from .models import User, Order, OrderCake


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'phone', 'email', ]


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ['address', 'date', 'time', 'delivcomments', ]


class CakeSerializer(ModelSerializer):

    class Meta:
        model = OrderCake
        fields = ['levels', 'form', 'topping', 'berries', 'decor', 'words', 'comment', 'cost', ]


def register_user(request):
    if 'name' in request.POST or 'email' in request.POST:
        User.objects.update_or_create(
            phone=request.POST['phone'],
            defaults={
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
            },
        )
    else:
        User.objects.get_or_create(phone=request.POST['phone'])
    return redirect('lk', request.POST['phone'])


def profile(request, phone):
    user = User.objects.get(phone=phone)

    return render(request, 'lk.html', {'user': user})


@api_view(['POST'])
def register_order(request):
    print(request.data)
    cake_serializer = CakeSerializer(data=request.data)
    cake_serializer.is_valid(raise_exception=True)
    order_serializer = OrderSerializer(data=request.data)
    order_serializer.is_valid(raise_exception=True)
    user_serializer = UserSerializer(data=request.data)
    user_serializer.is_valid()
    # return redirect('start_page')
    return Response()


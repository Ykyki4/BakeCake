from django.shortcuts import render, redirect
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from .forms import AuthForm
from .models import User, Order, OrderCake


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'phone', 'email']


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ['address', 'date', 'time', 'delivcomments', ]


class CakeSerializer(ModelSerializer):

    class Meta:
        model = OrderCake
        fields = ['levels', 'form', 'topping', 'berries', 'decor', 'words', 'comment', 'cost', ]


def index(request):
    auth_form = AuthForm

    return render(request, 'index.html', {'auth_form': auth_form})


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
        if request.POST['code'] == '1234':
            User.objects.get_or_create(phone=request.POST['phone'])
        else:
            return redirect('start_page')
    return redirect('lk', request.POST['phone'])


def profile(request, phone):
    user = User.objects.get(phone=phone)

    return render(request, 'lk.html', {'user': user})


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    request_payload = request.data
    cake_serializer = CakeSerializer(data=request_payload)
    cake_serializer.is_valid(raise_exception=True)
    order_serializer = OrderSerializer(data=request_payload)
    order_serializer.is_valid(raise_exception=True)
    user_serializer = UserSerializer(data=request_payload)
    user_serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        phone=user_serializer.validated_data['phone'],
        defaults={
            'name': user_serializer.validated_data['name'],
            'email': user_serializer.validated_data['email'],
        },
    )
    order, _ = Order.objects.get_or_create(
        address=order_serializer.validated_data['address'],
        date=order_serializer.validated_data['date'],
        time=order_serializer.validated_data['time'],
        delivcomments=order_serializer.validated_data.get('delivcomments', ''),
        user=user
    )
    OrderCake.objects.create(
        levels=cake_serializer.validated_data['levels'],
        form=cake_serializer.validated_data['form'],
        topping=cake_serializer.validated_data['topping'],
        berries=cake_serializer.validated_data['berries'],
        decor=cake_serializer.validated_data['decor'],
        words=cake_serializer.validated_data.get('words', ''),
        comment=cake_serializer.validated_data.get('comment', ''),
        cost=cake_serializer.validated_data['cost'],
        order=order
    )
    return redirect('start_page')
    # return Response()


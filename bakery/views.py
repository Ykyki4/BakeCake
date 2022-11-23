from django.shortcuts import render, redirect

from .models import User


def register_user(request):
    User.objects.create(phone=request.GET['REG'])
    return redirect('lk')

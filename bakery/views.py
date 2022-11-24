from django.shortcuts import render, redirect

from .models import User


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

def register_order(request):
    pass
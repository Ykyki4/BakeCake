from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    name = models.CharField('Имя', max_length=25, blank=True)
    phone = PhoneNumberField(verbose_name='Номер телефона', unique=True)
    email = models.EmailField(verbose_name='Электронная почта', blank=True)


class Order(models.Model):
    address = models.CharField('Адрес', max_length=150)
    date_time = models.DateTimeField('Время и день доставки')
    delivcomment = models.TextField('Комментарий к доставке')
    user = models.ForeignKey(User, verbose_name='Пользователь совершивший заказ', related_name='orders')
from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    name = models.CharField('Имя', max_length=25, blank=True)
    phone = PhoneNumberField(verbose_name='Номер телефона', unique=True)
    email = models.EmailField(verbose_name='Электронная почта', blank=True)


class Order(models.Model):
    address = models.CharField('Адрес', max_length=150)
    date = models.DateField('Дата доставки')
    time = models.TimeField('Время доставки')
    delivcomments = models.TextField('Комментарий к доставке', blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь совершивший заказ',
        related_name='orders'
    )


class OrderCake(models.Model):
    LEVELS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    FORMS = [
        ('1', 'Круг'),
        ('2', 'Квадрат'),
        ('3', 'Прямоугольник'),
    ]
    TOPPINGS = [
        ('1', 'Без'),
        ('2', 'Белый соус'),
        ('3', 'Карамельный'),
        ('4', 'Кленовый'),
        ('5', 'Черничный'),
        ('6', 'Молочный шоколад'),
        ('7', 'Клубничный'),
    ]
    BERRIES = [
        ('1', 'Ежевика'),
        ('2', 'Малина'),
        ('3', 'Голубика'),
        ('4', 'Клубника'),
    ]
    DECORS = [
        ('1', 'Фисташки'),
        ('2', 'Безе'),
        ('3', 'Фундук'),
        ('4', 'Пекан'),
        ('5', 'Маршмеллоу'),
        ('6', 'Марципан'),
    ]

    levels = models.CharField(
        'Уровни',
        max_length=2,
        choices=LEVELS,
    )

    form = models.CharField(
        'Форма',
        max_length=15,
        choices=FORMS,
    )

    topping = models.CharField(
        'Топпинг',
        max_length=20,
        choices=TOPPINGS,
    )

    berries = models.CharField(
        'Ягоды',
        max_length=10,
        choices=BERRIES,
        blank=True,
    )

    decor = models.CharField(
        'Декор',
        max_length=15,
        choices=DECORS,
        blank=True,
    )

    words = models.CharField('Надпись на торте', max_length=100, blank=True)
    comment = models.TextField('Комментарий', blank=True)

    cost = models.PositiveIntegerField('Стоимость торта', validators=[MinValueValidator(0)])

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='cake'
    )

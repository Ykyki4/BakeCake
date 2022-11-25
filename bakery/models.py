from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    name = models.CharField('Имя', max_length=25, blank=True)
    phone = PhoneNumberField(verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Электронная почта', blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.id} {self.user.name} {self.address}'


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
        related_name='cakes'
    )

    class Meta:
        verbose_name = 'торт'
        verbose_name_plural = 'торты'

    def __str__(self):
        return f'Торт для {self.order.user.name}'


class Payment(models.Model):
    PENDING = 'pending'
    WAITING = 'waiting'
    SUCCEEDED = 'succeeded'
    CANCELED = 'canceled'
    STATUSES = [
        (WAITING, 'Ожидает оплаты'),
        (SUCCEEDED, 'Оплачен'),
        (CANCELED, 'Платеж отклонен'),
    ]
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        verbose_name='Заказ',
        related_name='payments',
    )
    created_at = models.DateTimeField(
        'Создан в',
        default=timezone.now,
    )
    yookassa_payment_id = models.CharField(
        'ID платежа Юкасса',
        max_length=80,
        blank=True
    )
    status = models.CharField(
        'Статус заказа',
        max_length=20,
        choices=STATUSES,
        default=PENDING,
        db_index=True,
    )

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return f'Платеж по заказу {self.order.id}'

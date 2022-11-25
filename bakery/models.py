from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The given email must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, is_staff=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', blank=True)
    name = models.CharField('Имя', max_length=100, blank=True)
    phone = PhoneNumberField(verbose_name='Номер телефона', unique=True)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    is_active = models.BooleanField('Активный', default=True)
    is_staff = models.BooleanField('Менеджер', default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

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

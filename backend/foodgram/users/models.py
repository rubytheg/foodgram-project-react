from django.db import models
from django.contrib.auth.models import AbstractUser
from recipes.models import Recipe

class CustomUser(AbstractUser):
    #класс пользователя

    CHOICES_ROLE = ('user', 'admin')

    username = models.CharField(max_length=40, verbose_name="Имя пользователя", unique=True)
    email = models.EmailField(max_length=100, verbose_name="E-mail пользователя", unique=True)
    password = models.CharField(max_length=100, verbose_name="Пароль")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    recipes = models.ManyToManyField(Recipe, verbose_name="Рецепты")
    role = models.CharField(default='user', verbose_name="Роль пользователя", choice=CHOICES_ROLE)

    is_subscribed = models.BooleanField(
        verbose_name=_('Подписаться на автора'),
        blank=True,
        default=False)

    subscribers = models.ManyToManyField(
        'CustomUser',
        symmetrical=False,
        through="Subscription",
        through_fields=["user, subscriber"])

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'])
        ]

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь", related_name='subscribers')
    subscriber = models.ForeignKey(CustomUser, verbose_name="Подписчик", related_name='subscribed_to')
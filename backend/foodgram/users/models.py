from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    #модель пользователя
    USER = 'user'
    ADMIN = 'admin'
    CHOICES_ROLE = (USER, ADMIN)

    username = models.CharField(max_length=40, verbose_name=_("Имя пользователя"), unique=True)
    email = models.EmailField(max_length=100, verbose_name=_("E-mail пользователя"), unique=True)
    password = models.CharField(max_length=100, verbose_name=_("Пароль"))
    first_name = models.CharField(max_length=50, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=50, verbose_name=_("Фамилия"))
    role = models.CharField(default=USER, verbose_name=_("Роль пользователя"), choice=CHOICES_ROLE)
    slug = models.SlugField(unique=True)

    is_subscribed = models.BooleanField(
        verbose_name=_('Подписаться на автора'),
        blank=True,
        default=False)

    subscribers = models.ManyToManyField(
        "self",
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
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('id',)

class Subscription(models.Model):
    #through-модель подписки
    user = models.ForeignKey(
        CustomUser,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name='subscribers')

    subscriber = models.ForeignKey(
        CustomUser,
        verbose_name=_("Подписчик"),
        on_delete=models.CASCADE,
        related_name='subscribed_to')

    class Meta:
        verbose_name = _('Подписчик')
        verbose_name_plural = _('Подписчики')
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(fields=['user','subscriber'])
        ]

    def __str__(self):
        return f'{self.user} >> {self.subscriber}'
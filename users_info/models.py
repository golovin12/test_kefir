from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class UserModel(AbstractBaseUser):
    login_validator = UnicodeUsernameValidator()
    login = models.CharField(
        max_length=150,
        unique=True,
        help_text='Обязательное. 150 символов или меньше. Только: буквы, числа и @/./+/-/_',
        validators=[login_validator],
        error_messages={'unique': "Такое имя пользователя уже занято.", },
        verbose_name='Логин',
    )
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта', unique=True,
                              error_messages={'unique': 'Данная почта привязана к другому аккаунту.', })
    phone = models.CharField(verbose_name='Телефон', blank=True,
                             error_messages={'unique': 'Данный номер привязан к другому аккаунту.', }, max_length=16)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    is_admin = models.BooleanField(default=False, verbose_name='Админ',
                                   help_text='Установите в True, если хотите сделать пользователя админом')
    birthday = models.DateField(verbose_name='Дата рождения', help_text='Указывайте в формате дд.мм.гггг', blank=True,
                                null=True)
    city = models.ForeignKey('CityModel', blank=True, on_delete=models.SET_NULL, null=True)
    additional_info = models.TextField(blank=True, verbose_name='Дополнительная информация')
    other_name = models.CharField(max_length=150, blank=True, verbose_name='Отчество',
                                  help_text='Не обязательное поле. Максимальная длина - 150 символов')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ('date_joined',)

    def get_absolute_url(self):
        return reverse("api_users_control:private_user_edit", args=[self.id])

    def __str__(self):
        return self.login


class CityModel(models.Model):
    name = models.CharField(max_length=150, verbose_name='Город', unique=True)

    def __str__(self):
        return self.name

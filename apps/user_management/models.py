from django.db import models
from django.urls import reverse

from apps.services.utils import custom_slugify


class Profile(models.Model):
    """
    Модель для хранения информации о пользователе.
    """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                                related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    description = models.TextField(blank=True, null=True, verbose_name='Информация о себе')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name='Слаг')

    class Meta:
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.user.username}'

# python manage.py shell_plus --print-sql
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser

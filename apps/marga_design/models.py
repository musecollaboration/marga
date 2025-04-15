from django.db import models
from django.urls import reverse

from apps.services.models import AutoSlugMixin
from apps.services.utils import ProjectImagePath


class Project(AutoSlugMixin):
    """Модель для проектов"""
    title = models.CharField(max_length=255, verbose_name='Название проекта')
    description = models.TextField(verbose_name='Информация о проекте')
    price = models.IntegerField(blank=True, null=True, verbose_name='Цена проекта')
    plan_image = models.ImageField(upload_to=ProjectImagePath('plan_images'), blank=True, null=True,
                                   verbose_name='Изображение схемы проекта')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',
                                   help_text='Дата создания проекта')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', help_text='Дата обновления проекта')
    published = models.BooleanField(default=True, verbose_name='Статус',
                                    help_text='Убрать галочку если нужно снять с публикации')
    # top_rating = models.BooleanField(default=False, verbose_name='Рейтинг', help_text='Публикации для главной страницы')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Neva проект'
        verbose_name_plural = 'Neva проекты'

    def get_absolute_url(self):
        return reverse('marga_design:project', kwargs={'slug': self.slug})


class Parameter(AutoSlugMixin):
    """Модель для параметров"""
    title = models.CharField(max_length=255, unique=True, verbose_name='Параметр')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return self.title


class ProjectParameter(models.Model):
    """Связь параметров и проектов"""
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='parameters_set', verbose_name='Параметры')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_parameters_set')

    class Meta:
        verbose_name = 'Параметр проекта'
        verbose_name_plural = 'Параметры проектов'
        constraints = [
            models.UniqueConstraint(fields=['parameter', 'project'], name='unique_project_parameter')
        ]

    def __str__(self):
        return f"{self.project.title} — {self.parameter.title}"


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=ProjectImagePath('images'), verbose_name='Изображения')

    class Meta:
        verbose_name = 'Фотография проекта'
        verbose_name_plural = 'Фотографии проекта'

    @property
    def title(self):
        return self.project.title

    def __str__(self):
        return f'Изображение для: {self.project.title}'

# python manage.py shell_plus --print-sql
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser

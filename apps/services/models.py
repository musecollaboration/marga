from django.db import models
from slugify import slugify


class AutoSlugMixin(models.Model):
    """
    Миксин для создания слага
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name='URL',
                            help_text='Поле слаг заполняется автоматически')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

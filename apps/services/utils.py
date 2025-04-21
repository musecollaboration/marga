import uuid

from django.utils.deconstruct import deconstructible
from slugify import slugify


@deconstructible
class ProjectImagePath:
    def __init__(self, field_name: str):
        self.field_name = field_name

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        unique_name = uuid.uuid4()
        safe_title = slugify(instance.title)
        return f'projects/{self.field_name}/{safe_title}/{unique_name}.{ext}'


def custom_slugify(instance, slug) -> str:
    """
    Функция для создания слага из строки.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid.uuid4().hex[:8]}'
    return unique_slug

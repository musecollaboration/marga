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


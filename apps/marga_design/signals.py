import shutil
from pathlib import Path

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from slugify import slugify

from marga import settings
from .models import AutoSlugMixin, Project, ProjectImage, BlogPost, BlogPostImage


@receiver(pre_save, sender=Project)
def update_slug_and_rename_project_folders(sender, instance, **kwargs):
    """Обновление slug и переименование папок проекта при изменении названия проекта"""
    if not issubclass(sender, AutoSlugMixin):
        return

    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_slug = old_instance.slug
    new_slug = slugify(instance.title)

    if old_slug != new_slug:
        base_dirs = [
            Path(settings.MEDIA_ROOT) / 'projects' / 'images',
            Path(settings.MEDIA_ROOT) / 'projects' / 'plan_images',
        ]

        for base_dir in base_dirs:
            old_path = base_dir / old_slug
            new_path = base_dir / new_slug

            if old_path.exists():
                try:
                    old_path.rename(new_path)
                    print(f"[✓] Папка {old_path} переименована в {new_path}.")
                except Exception as e:
                    print(f"[!] Ошибка при переименовании {old_path} в {new_path}: {e}")

        # Обновление plan_image
        if instance.plan_image and old_slug in instance.plan_image.name:
            instance.plan_image.name = instance.plan_image.name.replace(old_slug, new_slug)

        # Обновление ProjectImage.image
        project_images = ProjectImage.objects.filter(project=instance, image__contains=old_slug)
        for img in project_images:
            try:
                img.image.name = img.image.name.replace(old_slug, new_slug)
                img.save(update_fields=['image'])
                print(f"[✓] Изображение {img.image.name} обновлено.")
            except Exception as e:
                print(f"[!] Ошибка при обновлении изображения {img.image.name}: {e}")


@receiver(post_delete, sender=Project)
def delete_project_files(sender, instance, **kwargs):
    """Удаляем папки проекта из media при удалении проекта"""
    if instance.slug:
        base_dirs = [
            Path(settings.MEDIA_ROOT) / 'projects' / 'images' / instance.slug,
            Path(settings.MEDIA_ROOT) / 'projects' / 'plan_images' / instance.slug,
        ]

        for folder in base_dirs:
            if folder.exists():
                try:
                    shutil.rmtree(folder)
                    print(f'[✓] Папка {folder} успешно удалена.')
                except Exception as e:
                    print(f"[!] Ошибка при удалении папки {folder}: {e}")


@receiver(post_delete, sender=ProjectImage)
def delete_images(sender, instance, **kwargs):
    """
    Удаляет изображение из файловой системы при удалении объекта ProjectImage.
    """
    image = instance.image
    if image and image.path:
        try:
            file_path = Path(image.path)
            if file_path.exists():
                file_path.unlink()
                print(f"[✓] Файл {file_path} успешно удалён.")
        except Exception as e:
            print(f"[!] Ошибка при удалении файла {image.path}: {e}")


@receiver(pre_save, sender=BlogPost)
def update_slug_and_rename_project_folders(sender, instance, **kwargs):
    """Обновление slug и переименование папок при изменении slug блога"""
    if not issubclass(sender, AutoSlugMixin):
        return

    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_slug = old_instance.slug
    new_slug = slugify(instance.title)

    if old_slug != new_slug:
        base_dirs = [
            Path(settings.MEDIA_ROOT) / 'projects' / 'blog_images',
        ]

        for base_dir in base_dirs:
            old_path = base_dir / old_slug
            new_path = base_dir / new_slug

            if old_path.exists():
                try:
                    old_path.rename(new_path)
                    print(f"[✓] Папка {old_path} переименована в {new_path}.")
                except Exception as e:
                    print(f"[!] Ошибка при переименовании {old_path} в {new_path}: {e}")


@receiver(post_delete, sender=BlogPost)
def delete_project_files(sender, instance, **kwargs):
    """Удаляем папки проекта из media при удалении проекта"""
    if instance.slug:
        base_dirs = [
            Path(settings.MEDIA_ROOT) / 'projects' / 'blog_images' / instance.slug,
        ]

        for folder in base_dirs:
            if folder.exists():
                try:
                    shutil.rmtree(folder)
                    print(f'[✓] Папка {folder} успешно удалена.')
                except Exception as e:
                    print(f"[!] Ошибка при удалении папки {folder}: {e}")


@receiver(post_delete, sender=BlogPostImage)
def delete_images(sender, instance, **kwargs):
    """Удаляет изображение из файловой системы при удалении объекта BlogPostImage"""
    image = instance.image
    if image and image.path:
        try:
            file_path = Path(image.path)
            if file_path.exists():
                file_path.unlink()
                print(f"[✓] Файл {file_path} успешно удалён.")
        except Exception as e:
            print(f"[!] Ошибка при удалении файла {image.path}: {e}")

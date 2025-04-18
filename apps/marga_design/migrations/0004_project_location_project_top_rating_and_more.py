# Generated by Django 5.2 on 2025-04-15 07:59

import apps.services.utils
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marga_design', '0003_alter_parameter_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='location',
            field=models.CharField(max_length=255, null=True, verbose_name='Локация'),
        ),
        migrations.AddField(
            model_name='project',
            name='top_rating',
            field=models.BooleanField(default=False, help_text='Публикации на главной страницы', verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='project',
            name='published',
            field=models.BooleanField(default=True, help_text='Убрать галочку если нужно снять с публикации', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='image',
            field=models.ImageField(upload_to=apps.services.utils.ProjectImagePath('images'), verbose_name='Изображения'),
        ),
        migrations.AlterField(
            model_name='projectparameter',
            name='parameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters_set', to='marga_design.parameter', verbose_name='Параметры'),
        ),
    ]

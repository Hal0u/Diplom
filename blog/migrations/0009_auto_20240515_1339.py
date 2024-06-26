# Generated by Django 3.2.4 on 2024-05-15 08:39

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_alter_post_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категорию', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Пост', 'verbose_name_plural': 'Пост'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепт'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'тэг', 'verbose_name_plural': 'Теги'},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='website',
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post', to='blog.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='articles/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Отображение на сайте'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='post', to='blog.Tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cook_time',
            field=models.PositiveIntegerField(default=0, verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='directions',
            field=ckeditor.fields.RichTextField(verbose_name='Инструкции'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=ckeditor.fields.RichTextField(verbose_name='Ингридиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название блюда'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='prep_time',
            field=models.PositiveIntegerField(default=0, verbose_name='Время на подготовку'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='serves',
            field=models.CharField(max_length=50, verbose_name='Время подачи'),
        ),
    ]

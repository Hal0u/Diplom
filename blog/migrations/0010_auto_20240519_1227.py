# Generated by Django 3.2.4 on 2024-05-19 07:27

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20240515_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loginAccount', models.CharField(default='', max_length=60, verbose_name='Логин')),
                ('passwordAccount', models.CharField(default='', max_length=60, verbose_name='Пароль')),
                ('roleTitleAccount', models.CharField(default='', max_length=50, verbose_name='Название роли')),
            ],
            options={
                'verbose_name': 'Аккаунты',
                'verbose_name_plural': 'Аккаунты',
            },
            managers=[
                ('objectsAccount', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('objectsPost', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Рецепты', to='blog.post'),
        ),
    ]

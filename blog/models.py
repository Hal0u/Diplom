from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

class Account(models.Model):
    loginAccount = models.CharField('Логин', max_length=60, default="") # Ключевой параметр loginAccount
    passwordAccount = models.CharField('Пароль', max_length=60, default="")
    roleTitleAccount = models.CharField('Название роли', max_length=50, default="")
    objectsAccount = models.Manager()

    def __str__(self):
        return self.loginAccount

    class Meta:
        verbose_name = 'Аккаунты'
        verbose_name_plural = 'Аккаунты'




class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    # objectsCategory = models.Manager()
    parent = TreeForeignKey(
        'self',
        related_name="children",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'



    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']



class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Теги'


class Post(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='articles/', verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание')
    administrationVerified = models.BooleanField(verbose_name='Подтверждение админа', default=False)
    objectsPost = models.Manager()
    category = models.ForeignKey(
        Category,
        related_name="post",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(Tag, related_name="post", verbose_name='Теги')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Отображение на сайте')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_single", kwargs={"slug": self.category.slug, "post_slug": self.slug})

    def get_recipes(self):
        return self.Рецепты.all()

    def get_comments(self):
        return self.comment.all()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пост'


class Recipe(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название блюда')
    serves = models.CharField(max_length=50, verbose_name='Время подачи')
    prep_time = models.PositiveIntegerField(default=0, verbose_name='Время на подготовку')
    cook_time = models.PositiveIntegerField(default=0, verbose_name='Время приготовления')
    ingredients = RichTextField(verbose_name='Ингридиенты')
    directions = RichTextField(verbose_name='Инструкции')
    objectsRecipe = models.Manager()
    post = models.ForeignKey(
        Post,
        related_name="Рецепты",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепт'


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    create_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, related_name="comment", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'


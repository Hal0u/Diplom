from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.text import slugify
from .models import Comment, Account, Post, Category, Tag, Recipe

from django import template

register = template.Library()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['create_at', 'post']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email'}),
            'website': forms.TextInput(attrs={'placeholder': 'website'}),
            'message': forms.Textarea(attrs={'placeholder': 'message'})
            
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'text', 'category', 'tags', 'slug']
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure the slug is unique
            unique_slug = self.slug
            num = 1
            while Post.objectsPost.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'serves', 'prep_time', 'cook_time', 'ingredients', 'directions']

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=200, label='Название')
    image = forms.ImageField(label='Изображение', required=False)
    text = forms.CharField(widget=forms.Textarea, label='Описание')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), label='Теги', required=False)
    slug = forms.SlugField(max_length=200, label='Отображение на сайте', required=False)
    recipe_name = forms.CharField(max_length=100, label='Название блюда')
    serves = forms.CharField(max_length=50, label='Время подачи')
    prep_time = forms.IntegerField(label='Время на подготовку')
    cook_time = forms.IntegerField(label='Время приготовления')
    ingredients = forms.CharField(widget=forms.Textarea, label='Ингридиенты')
    directions = forms.CharField(widget=forms.Textarea, label='Инструкции')

    def save(self, user):
       
        post_data = {
            'author': user,
            'title': self.cleaned_data['title'],
            'image': self.cleaned_data['image'],
            'text': self.cleaned_data['text'],
            'category': self.cleaned_data['category'],
            'slug': self.cleaned_data['slug'],
        }
        post = Post.objectsPost.create(**post_data)
        post.tags.set(self.cleaned_data['tags'])
        
        recipe_data = {
            'name': self.cleaned_data['recipe_name'],
            'serves': self.cleaned_data['serves'],
            'prep_time': self.cleaned_data['prep_time'],
            'cook_time': self.cleaned_data['cook_time'],
            'ingredients': self.cleaned_data['ingredients'],
            'directions': self.cleaned_data['directions'],
            'post': post
        }
        Recipe.objectsRecipe.create(**recipe_data)


# class AddPostForm(forms.ModelForm):
#     category = forms.ModelChoiceField(queryset=Category.objects.all(),label='Категория')
#     tags = forms.ModelChoiceField(queryset=Tag.objects.all(),label='Тэг')


#     class Meta:
#         model = Post, Recipe
#         fields = ['title', 'image', 'text', name serves]
#         widgets = {
#             'title': forms.Textarea(attrs={'cols': 60, 'rows': 5}),
#             'image': forms.ClearableFileInput(),
#             'text': forms.Textarea(attrs={'cols': 60, 'rows': 1}),

#         }

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['username'].widget.attrs.update({'class': 'form-control'})
       self.fields['password1'].widget.attrs.update({'class':'form-control'})
       self.fields['password2'].widget.attrs.update({'class':'form-control'})

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['username'].widget.attrs.update({'class': 'form-control'})
       self.fields['password'].widget.attrs.update({'class':'form-control'})



@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})
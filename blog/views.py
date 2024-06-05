from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Recipe
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CommentForm, UserRegistrationForm, UserLoginForm, AddPostForm
from django.core.paginator import Paginator


def search(request):
    query = request.GET.get('q')

    if query:
        post_lsit = Post.objectsPost.filter(title__icontains=query, administrationVerified=True)
    else:
        post_lsit = Post.objectsPost.all()
    return render(request, 'blog/home.html', {'post_list': post_lsit, 'query': query})


class HomeView1(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/home.html"

def myAccount(request):
    if request.method == 'POST':
        formMyAccount = UserRegistrationForm(request.POST)
        if formMyAccount.is_valid():
            formMyAccount.save()
            username = formMyAccount.cleaned_data.get('username')
            return redirect('/user_login')  # Перенаправление на страницу входа после успешной регистрации
    else:
        formMyAccount = UserRegistrationForm()
    return render(request, "blog/registration.html", {'formMyAccount': formMyAccount})

def logout_user(request):
    logout(request)
    return redirect('/user_login')

def user_login(request):
    print('login')
    if request.method == 'POST':
        formMyAccountAuto = UserLoginForm(data=request.POST)
        if formMyAccountAuto.is_valid():
            username = formMyAccountAuto.cleaned_data.get('username')
            password = formMyAccountAuto.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        formMyAccountAuto = UserLoginForm()
    return render(request, 'blog/login.html', {'formMyAccountAuto': formMyAccountAuto})

class HomeView(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/home.html"
    def get_queryset(self):
        return Post.objectsPost.filter(administrationVerified=True).select_related('category')




class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objectsPost.filter(category__slug=self.kwargs.get("slug"), administrationVerified=True).select_related('category')


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

def AddPost(request):
    rev = Post.objectsPost.filter(administrationVerified=True).all()
    paginator = Paginator(rev, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_authenticated:
                form.save(user=request.user)
            form = AddPostForm()
            try:
                return redirect('/')
                print('nothing')
            except Exception as e:
                form.add_error(None, f'Ошибка добавления рецепта:{e}')
    else:
        form = AddPostForm()
        print(form)
    context = {
        'form': form,
        'rev': rev,
        'page_obj': page_obj,
    }
    return render(request, "blog/addpost.html", context=context)

class CreateComment(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


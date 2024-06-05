from django.urls import path


from . import views


urlpatterns = [
    path('search/', views.search, name='search'),
    path('comment/<int:pk>/', views.CreateComment.as_view(), name="create_comment"),
    path('<slug:slug>/<slug:post_slug>/', views.PostDetailView.as_view(), name="post_single"),
    path('<slug:slug>/', views.PostListView.as_view(), name="post_list"),
    path('register', views.myAccount, name='Registration'),
    path('logout', views.logout_user, name='UserLogout'),
    path('user_login', views.user_login, name='userLogin'),
    path('', views.HomeView.as_view(), name="home"),
    path('addPost', views.AddPost, name="addPost"),
]
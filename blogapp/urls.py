from django.urls import path, include
from .views import BlogListView, BlogDetailView, ReviewCreateView, CommentCreateView, BlogCreateView, CustomLoginView
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blogapp'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path("register/", views.register, name="register"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('blog/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='edit_blog'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='delete_blog'),
]

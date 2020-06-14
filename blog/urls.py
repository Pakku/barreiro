from . import views
from django.urls import path
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('categoria/<slug:slug>', views.CategoryPostList.as_view(), name='category'),
    path('etiqueta/<slug:slug>', views.TagPostList.as_view(), name='tag'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('feed/rss', LatestPostsFeed(), name='post_feed'),
]

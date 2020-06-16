from django.urls import path
from .views import (
    blog,
    search,
    single,
    PostListView,
    UserPostListView,
    CategoryPostListView, PostCreateView, PostUpdateView,
    PostDeleteView
    )


urlpatterns = [
    #path('blog/', blog, name='blog'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('blog/new/', PostCreateView.as_view(), name='post-create'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('category/<str:name>', CategoryPostListView.as_view(), name='category-posts'),
    #path('blog/<int:pk>-<str:slug>/', PostDetailView.as_view(), name='single'),
    path('blog/<int:pk>-<str:slug>/', single, name='single'),
    path('blog/<int:pk>-<str:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('blog/<int:pk>-<str:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('blog/search/', search, name='blog-search'),
]
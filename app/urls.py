from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name="index"),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('author/<slug:slug>', views.author_page, name='author_page'),
    path('search/', views.search_post, name='search_page'),
    path('about/', views.about_page, name='about_page'),
    path('accounts/register/', views.register_user, name='register'),
    path('bookmark/<slug:slug>', views.bookmark_post, name='bookmark_post'),
    path('like/<slug:slug>', views.like_post, name='like_post'),
]

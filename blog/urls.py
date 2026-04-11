from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('hot/', views.hot_posts, name='hot_posts'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/<str:username>/', views.chat_with, name='chat_with'),
    path('messages/<str:username>/new/', views.get_new_messages, name='get_new_messages'),
    path('user/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('user/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('user/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('user/<str:username>/following/', views.following_list, name='following_list'),
]

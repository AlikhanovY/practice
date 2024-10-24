from django.urls import path

from . import views

urlpatterns =[
    path('posts/', views.list_posts, name="list_posts"), 
    path('posts/<int:pk>', views.post_num, name="post_num"),
    path('posts/create', views.create_post, name='create_post'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post-delete'),
    path('post/<int:post_id>/comments/', views.comment_list, name='comment_list'),
    path('post/<int:post_id>/comments/add/', views.add_comment, name='add_comment'),
    
]


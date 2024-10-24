from django.urls import path

from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/posts/', views.user_posts, name='profile_posts'),
    path('profile/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('profile/<int:user_id>/unfollow/', views.unfollow_user, name='unfollow_user'),
]

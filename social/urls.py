from django.urls import path
from . import views


urlpatterns = [

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'profile/<str:username>/',
        views.profile,
        name='profile'
    ),

    path(
        '',
        views.feed,
        name='feed'
    ),

    path(
        'post/create/',
        views.create_post,
        name='create_post'
    ),

    path(
        'post/<int:post_id>/edit/',
        views.edit_post,
        name='edit_post'
    ),

    path(
        'post/<int:post_id>/delete/',
        views.delete_post,
        name='delete_post'
    ),
        path(
        'post/<int:post_id>/like/',
        views.like_post,
        name='like_post'
    ),

    path(
        'post/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),

    path(
        'follow/<str:username>/',
        views.follow_user,
        name='follow_user'
    ),

    path(
        'profile/<str:username>/followers/',
        views.followers_list,
        name='followers'
    ),

    path(
        'profile/<str:username>/following/',
        views.following_list,
        name='following'
    ),
]
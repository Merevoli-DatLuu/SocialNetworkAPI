from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import post_list, post_detail, likepost_detail, comment_list_sub, comment_list

urlpatterns = [
    path('post',                                        post_list,          name='post_list'),
    path('post/<int:pk>',                               post_detail,        name='post_detail'),
    path('like-post/<int:post_id>',                     likepost_detail,    name='likepost'),
    path('comment/<int:pk>',                            comment_list,       name='comment_list'),
    path('comment/<int:post_id>/sub/<int:comment_id>',  comment_list_sub,   name='comment_list_sub')
]
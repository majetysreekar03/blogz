from django.urls import path
from . import views

app_name='app_blog'

urlpatterns = [
   path('',views.Bloglist.as_view(),name='blog_list'),
   path('create/',views.create_blog.as_view(),name='create_blog'),
   path('details/<slug:slug>',views.blog_details,name='blog_details'),
   path('liked/<pk>',views.liked,name='liked_post'),
   path('unliked/<pk>/',views.unliked,name='unliked_post'),
   path('myblogs/',views.myblogs.as_view(),name='myblogs'),
   path('editblog/<pk>/',views.editblog.as_view(),name='editblog'),
   path('blog_details_not_loggedin/<slug:slug>',views.blog_details_not_loggedin,name='blog_details_not_loggedin'),
   path('signin_for_comment/<slug:slug>',views.signin_for_comment,name='signin_for_comment'),
]

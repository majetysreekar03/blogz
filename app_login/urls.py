from django.urls import path
from . import views

app_name='app_login'

urlpatterns = [
   path('signup/',views.signup,name='signup'),
   path('signin/',views.login_page,name='signin'),
   path('logout/',views.logout_user,name='logout'),
   path('profile/',views.profile,name='profile'),
   path('change_profile/',views.user_change,name='user_change'),
   path('password/',views.password_change,name='password_change'),
   path('change_profile_img/',views.add_profile_pic,name="add_profile_pic"),
   path('change_pic/',views.change_profile_pic,name="change_profile_pic" )
]

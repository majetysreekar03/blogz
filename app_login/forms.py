from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from app_login.models import UserProfile

class signup_form(UserCreationForm):
    email=forms.EmailField(label="Email Adress",required=True)
    class Meta:
       model=User
       fields=('username','email','password1','password2')

class change_profile(UserChangeForm):
    class Meta:
        model=User
        fields=('username','email','first_name','last_name','password')

class profile_pic(forms.ModelForm):
     class Meta:
        model = UserProfile
        fields=['profile_pic',]

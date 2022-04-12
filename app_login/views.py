from gettext import install
from operator import methodcaller
from urllib.request import HTTPRedirectHandler
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app_login.forms import profile_pic, signup_form,change_profile

# Create your views here.

def signup(request):
    form=signup_form()
    registered=False
    if request.method == 'POST':
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered=True
    diction={
        'form':form,
        'registered':registered
    }
    return render(request,'app_login/signup.html',context=diction)

def login_page(request):
    form=AuthenticationForm()
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            us=form.cleaned_data.get('username')
            pa=form.cleaned_data.get('password')
            user=authenticate(username=us,password=pa)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
    return render(request,'app_login/login.html',context={'form':form})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('app_login:signin'))


@login_required
def profile(request):
    diction={}
    return render(request,'app_login/profile.html',context=diction)

@login_required
def user_change(request):
    current_user=request.user
    form=change_profile(instance=current_user)
    if request.method=='POST':
        form = change_profile(request.POST,instance=current_user)
        if form.is_valid():
            form.save()
            form=change_profile(instance=current_user)
    diction={'form':form}
    return render(request,'app_login/change_profile.html',context=diction)

@login_required
def password_change(request):
    current_user=request.user
    change=False
    form=PasswordChangeForm(current_user)
    if request.method=='POST':
        form=PasswordChangeForm(current_user,data=request.POST)
        if form.is_valid():
            form.save()
            change=True
            return HttpResponseRedirect(reverse('app_login:signin'))
    return render(request,'app_login/password_change.html',context={'form':form,'change':change})

@login_required
def add_profile_pic(request):
    form = profile_pic()
    if request.method == 'POST':
        form=profile_pic(request.POST,request.FILES)
        if form.is_valid():
            user_obj=form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('app_login:profile'))
    return render(request,'app_login/pro_pic_add.html',context={'form':form})

@login_required
def change_profile_pic(request):
    form = profile_pic(instance=request.user.user_profile)
    if request.method=='POST':
        form = profile_pic(request.POST,request.FILES,instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app_login:profile'))
    return render(request,'app_login/pro_pic_add.html',context={'form':form})

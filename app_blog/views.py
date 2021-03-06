from distutils.log import error
from operator import truediv
from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import CreateView,UpdateView,ListView,DetailView,TemplateView,DeleteView
from .models import Blog,comment,Likes
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid 
from app_blog.forms import commentform
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate

# Create your views here.

class Bloglist(ListView):
    context_object_name= 'blogs'
    model=Blog
    template_name='app_blog/blog_list.html'
    queryset=Blog.objects.order_by("-publish_date")



class create_blog(LoginRequiredMixin,CreateView):
    model=Blog
    template_name='App_blog/create_blog.html'
    fields=('blog_title','blog_content','blog_image')

    def form_valid(self,form):
        blog_obj=form.save(commit=False)
        blog_obj.author=self.request.user
        title=blog_obj.blog_title
        blog_obj.slug= title.replace(" ","-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))

@login_required
def blog_details(request,slug):
    blog=Blog.objects.get(slug=slug)
    comment_form=commentform()
    already_liked=Likes.objects.filter(blog=blog,user=request.user)
    if already_liked:
               liked=True
    else :
               liked=False
    if request.method=='POST':
               comment_form=commentform(request.POST)
               if comment_form.is_valid():
                 comment=comment_form.save(commit=False)
                 comment.user=request.user
                 comment.blog=blog
                 comment.save()
                 return HttpResponseRedirect(reverse('app_blog:blog_details',kwargs={'slug':slug}))
    return render(request,'app_blog/blog_details.html',context={'blog':blog,'comment_form':comment_form,'liked':liked})

def blog_details_not_loggedin(request,slug):
    blog=Blog.objects.get(slug=slug)
    return render(request,'app_blog/blog_details_not_loggedin.html',context={'blog':blog})

@login_required
def liked(request,pk):
    blog=Blog.objects.get(pk=pk)
    user=request.user
    already_liked=Likes.objects.filter(blog=blog,user=user)
    if not already_liked:
        liked_post=Likes(blog=blog,user=user)
        liked_post.save()
        return HttpResponseRedirect(reverse('app_blog:blog_details',kwargs={'slug':blog.slug}))

@login_required
def unliked(request,pk):
    blog=Blog.objects.get(pk=pk)
    user=request.user
    already_liked= Likes.objects.filter(blog=blog,user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('app_blog:blog_details',kwargs={'slug':blog.slug}))
 
class myblogs(LoginRequiredMixin,TemplateView):
    template_name='app_blog/my_blogs.html'

class editblog(LoginRequiredMixin,UpdateView):
    model=Blog
    fields=('blog_title','blog_content','blog_image')
    template_name='app_blog/edit_blog.html'

    def get_success_url(self,**kwargs):
        return reverse_lazy('app_blog:blog_details',kwargs={'slug':self.object.slug})
 
def signin_for_comment(request,slug):
    form=AuthenticationForm()
    if request.method=='POST': 
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            us=form.cleaned_data.get('username')
            pa=form.cleaned_data.get('password')
            user=authenticate(username=us,password=pa)
            if user is not None:  
                login(request,user) 
                return HttpResponseRedirect(reverse('app_blog:blog_details',kwargs={'slug':slug}))   
    return render(request,'app_login/login.html',context={'form':form})
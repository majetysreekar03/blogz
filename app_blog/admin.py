from django.contrib import admin
from .models import Blog,comment,Likes
# Register your models here.

admin.site.register(Blog)
admin.site.register(comment)
admin.site.register(Likes)

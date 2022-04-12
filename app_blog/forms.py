from django import forms
from app_blog.models import Blog,comment

class commentform(forms.ModelForm):
    class Meta:
        model=comment
        fields=('comment',)
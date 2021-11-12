from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_author', 'post_category', 'choise_type', 'headline', 'text']

class SearchForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_author', 'headline']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
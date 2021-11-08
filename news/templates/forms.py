from django.forms import ModelForm
from news.models import Post, Category


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_author', 'post_category', 'choise_type', 'headline', 'text']


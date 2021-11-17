from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_author', 'post_category', 'choise_type', 'headline', 'text']

# class SearchForm(ModelForm):
#     class Meta:
#         model = Post
#         fields = ['post_author', 'headline']

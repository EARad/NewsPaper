from django_filters import FilterSet
from .models import Post


class PostsFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'headline': ['icontains'],
            'post_author': ['exact'],
            'date': ['gte'],
        }
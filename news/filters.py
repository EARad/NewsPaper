from django_filters import DateFilter, FilterSet
from .models import Post




class PostsFilter(FilterSet):
    time_of_creation = DateFilter

    class Meta:
        model = Post
        fields = {
            'headline': ['icontains'],
            'post_author': ['exact'],
            'date': ['gt'],
        }






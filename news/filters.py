from django_filters import filters, FilterSet
from .models import Post


class PostsFilter(FilterSet):
    headline = filters.CharFilter(label='Заголовок', lookup_expr='icontains')
    post_author = filters.CharFilter(label='Автор', lookup_expr='exact')
    date = filters.DateFilter(label='Дата', lookup_expr='gt')

    class Meta:
        model = Post
        fields = ['headline', 'post_author', 'date']



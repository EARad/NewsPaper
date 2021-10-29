from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date')

    # def date_new (self):
    #     date_n = Post.date
    #     return date_n.models.DateField

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_now'] = Post.date  # добавим переменную текущей даты time_now
    #     return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


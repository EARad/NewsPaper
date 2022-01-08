from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from .filters import PostsFilter
from .forms import PostForm, SearchForm


class Posts(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 10


class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.post_create',)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.post_update',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    ordering = ['-date']
    paginate_by = 10
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CategoryView(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    queryset = Category.objects.all()
    paginate_by = 10


@login_required
def subscribe_me(request, cat_id):
    user = request.user
    category = Category.objects.get(pk=cat_id)
    if request.user not in category.subscribers.all():
        category.subscribers.add(user)
    return redirect('/news/category/')


@login_required
def unsubscribe_me(request, cat_id):
    user = request.user
    category = Category.objects.get(pk=cat_id)
    if request.user in category.subscribers.all():
        category.subscribers.remove(user)
    return redirect('/news/category/')

from django.shortcuts import redirect, reverse, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .filters import PostsFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.mail import send_mail


# class SendMail(View):
#
#     def get(self, request, *args, **kwargs):
#         return render(request, 'make_mail.html', {})
#
#     def post(self, request, *args, **kwargs):
#         mail = Post(
#             headline = request.POST['headline'],
#             text = request.POST['text'],
#         )
#         mail.save()
#
#         # отправляем письмо
#         send_mail(
#             subject=f'{mail.headline}',
#             # заголовок будет в теме для удобства
#             message=mail.text,  # текст
#             from_email='zhenyaradchikov@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
#             recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
#         )
#
#         return redirect('mail:make_mail.html')


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
    permission_required = ('news.add_post',)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/'


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    ordering = ['-date']
    paginate_by = 10

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

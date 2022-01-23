from django.urls import path
from .views import Posts, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearch, CategoryView,\
    subscribe_me, unsubscribe_me
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', Posts.as_view(), name='posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('category/', cache_page(60*5)(CategoryView.as_view()), name='category'),
    path('category/subscribes/<int:cat_id>/', subscribe_me, name='subscribes'),
    path('category/unsubscribes/<int:cat_id>/', unsubscribe_me, name='unsubscribes'),
    ]
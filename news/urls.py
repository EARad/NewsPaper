from django.urls import path
from .views import Posts, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearch, CategoryView,\
    subscribe, unsubscribe


urlpatterns = [
    path('', Posts.as_view(), name='posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('category/', CategoryView.as_view(), name='category'),
    path('category/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('category/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
    ]
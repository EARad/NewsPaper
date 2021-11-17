from django.urls import path
from .views import Posts, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearch


urlpatterns = [
    path('', Posts.as_view(), name='posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
    ]
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, BecomeBloggerView, AuthorListView, HomeView, PostLikeView
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('new/', PostCreateView.as_view(), name='post_new'),
    path('articles/', PostListView.as_view(), name='post_list'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('become_blogger/', BecomeBloggerView.as_view(), name='become_blogger'),
    path('p/<str:username>/<slug:slug>/',
         PostDetailView.as_view(), name='post_detail'),
    path('p/<str:username>/<slug:slug>/edit',
         PostUpdateView.as_view(), name='post_edit'),
    path('p/<str:username>/<slug:slug>/delete',
         PostDeleteView.as_view(), name='post_delete'),
    path('p/<str:username>/<slug:slug>/like',
         PostLikeView.as_view(), name='post_like'),
]

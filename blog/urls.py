from .views import PostList, PostDetail
from django.urls import path

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('article/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
]

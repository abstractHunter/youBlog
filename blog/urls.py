from .views import PostList, PostDetail, PostCreate
from django.urls import path

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('new/', PostCreate.as_view(), name='post_new'),
    path('<str:username>/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
]

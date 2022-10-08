from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.


class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'home.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

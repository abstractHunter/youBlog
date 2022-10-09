from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post

# Create your views here.


class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'home.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'slug', 'content', 'status', 'tags']
    success_url = reverse_lazy('my_profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)

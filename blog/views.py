from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Post
from .forms import CommentForm
# Create your views here.


class PostListView(ListView):
    queryset = Post.objects.filter(published=True).order_by('-created_at')
    template_name = 'blog/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=self.kwargs['slug'])
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = post
            form.save()
        return redirect('post_detail', username=post.author, slug=self.kwargs['slug'])


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'published', 'tags']
    success_url = reverse_lazy('my_profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'published', 'tags']
    success_url = reverse_lazy('my_profile')

    def get(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('my_profile')
        return super().get(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('my_profile')

    def get(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('my_profile')
        return super().get(request, *args, **kwargs)

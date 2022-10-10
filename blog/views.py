from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Post

# Create your views here.


class PostListView(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'home.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'slug', 'content', 'status', 'tags']
    success_url = reverse_lazy('my_profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'slug', 'content', 'status', 'tags']
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

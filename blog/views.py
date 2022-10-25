from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from .models import Post, Tag
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

        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

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

    def get(self, request, *args, **kwargs):
        if not request.user.is_blogger:
            return redirect('become_blogger')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'published', 'tags']
    success_url = reverse_lazy('my_profile')

    def get(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('my_profile')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('my_profile')

    def get(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('my_profile')
        return super().get(request, *args, **kwargs)


class BecomeBloggerView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/become_blogger_confirm.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_blogger:
            return redirect('my_profile')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.user.is_blogger = True
        request.user.save()
        return redirect('my_profile')


class AuthorListView(ListView):
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        return get_user_model().objects.filter(is_blogger=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = self.get_queryset()
        return context

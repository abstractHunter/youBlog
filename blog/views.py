from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from .models import Post
from .forms import CommentForm, PostForm
# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.published_objects.order_by('-created_at')[:3]
        context["popular_posts"] = sorted(Post.published_objects.all(), key=lambda x: x.rating, reverse=True)[:3]
        context["popular_authors"] = sorted(get_user_model().authors.all(), key=lambda x: x.rating, reverse=True)[:3]
        return context


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
    form_class = PostForm
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
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('my_profile')

    def get(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('my_profile')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('my_profile')

    def get(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('my_profile')
        return super().get(request, *args, **kwargs)


class PostLikeView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(slug=self.kwargs['slug'])
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('post_detail', username=post.author, slug=self.kwargs['slug'])


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
        return get_user_model().authors.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = self.get_queryset()
        return context

from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login, logout
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm
from blog.models import Post

# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class SignInView(LoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class SignOutView(LogoutView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "accounts/profile.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        if self.kwargs.get("username"):
            user = get_user_model().objects.get(username=self.kwargs.get("username"))
        else:
            user = self.request.user

        context = super().get_context_data(**kwargs)
        context["user_profile"] = user
        context["posts"] = Post.objects.filter(author=user)
        return context

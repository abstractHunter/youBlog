from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login, logout
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm
from blog.models import Post

# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

    def get(self, request, *args, **kwargs):
        # if the user is already logged in, redirect to the home page
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # get the username and password from the form
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # check if the user already exists
        if get_user_model().objects.filter(username=username).exists():
            message = "Cet utilisateur existe déjà"
            return render(request, "accounts/signup.html", {"message": message, "username": username})

        # check if the passwords match
        if password1 != password2:
            message = "Les mots de passe ne correspondent pas"
            return render(request, "accounts/signup.html", {"message": message, "username": username})

        # create the user and log the user in
        user = get_user_model().objects.create_user(
            username=username,
            password=password1,
        )
        login(request, user)

        return super().post(request, *args, **kwargs)


class SignInView(LoginView):
    template_name = "accounts/login.html"

    """ def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form) """

    def get(self, request, *args, **kwargs):
        # if the user is already logged in, redirect to the home page
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # get the username and password from the form
        username = request.POST.get("username")
        password = request.POST.get("password")

        # check if the user exists
        user = get_user_model().objects.filter(username=username).first()

        # if user does not exist, return an error message
        if user is None:
            message = "Cet utilisateur n'existe pas"
            return render(request, "accounts/login.html", {"message": message, "username": username})

        # if the password is incorrect, return an error message
        if not user.check_password(password):
            message = "Mot de passe incorrect"
            return render(request, "accounts/login.html", {"message": message, "username": username})

        # if the user exists and the password is correct, log the user in
        login(request, user)

        return super().post(request, *args, **kwargs)


class SignOutView(LogoutView):

    def get(self, request, *args, **kwargs):
        # if the user is not logged in, redirect to the home page
        if not request.user.is_authenticated:
            return redirect("home")

        # logout the user
        logout(request)
        return super().get(request, *args, **kwargs)


class ProfileView(DetailView):
    template_name = "accounts/profile.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # if the logged in user is viewing his own profile
        if self.kwargs.get("username"):
            user = get_user_model().objects.get(username=self.kwargs.get("username"))
            context["posts"] = Post.objects.filter(
                author=user).filter(published=True)
        # if the logged in user is viewing another user's profile
        else:
            user = self.request.user
            context["posts"] = Post.objects.filter(author=user)

        context["user_profile"] = user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "accounts/edit_profile.html"
    fields = ["username", "email", "first_name", "last_name"]
    success_url = reverse_lazy("my_profile")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

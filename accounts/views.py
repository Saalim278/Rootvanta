from django.shortcuts import render
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class RoleBasedLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse("admin:index")

        role = user.role

        if user.role in ["QA", "DEVELOPER", "MANAGER"]:
            return reverse("investigation_list")


        # if role == "QA":
        #     return reverse("home")

        # elif role == "DEVELOPER":
        #     return reverse("home")

        # elif role == "MANAGER":
        #     return reverse("home")

        return reverse("login")

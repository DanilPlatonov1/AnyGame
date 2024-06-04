from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'users/sign_up.html'
    success_url = reverse_lazy('users:login')


class LoginPage(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'


def logout_user(request):
    logout(request)
    return redirect('/')


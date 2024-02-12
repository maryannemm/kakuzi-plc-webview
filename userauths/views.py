from typing import Any
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from .forms import RegistrationForm, LoginForm, SubscribeForm
from .models import Subscribers, User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'userauths/sign-up.html'
    model = User
    form_class = RegistrationForm
    success_message = ' You have successfully registered.'
    redirect_authenticated_user=True
    success_url = reverse_lazy('core:index')


    def form_valid(self, form):
        # Your logic for handling a valid form submission goes here
        response = super().form_valid(form)

        # Access the username and email from the form
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')

        # Authenticate the user using email and password
        user = authenticate(self.request, username=email, password=form.cleaned_data.get('password1'))

        # Log in the authenticated user
        if user is not None:
            login(self.request, user)

        # Set the success message with the username
        self.success_message = self.success_message.format(username=username)

        return response
class MyLoginView(SuccessMessageMixin,LoginView):
    template_name = 'userauths/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm
    success_message='Logged in Successfully!'

    def get_success_url(self):
        return reverse_lazy('core:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)
    
class MyLogoutView(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy('core:index')
    
    def logout(self, request):
        messages.success(request, 'You have successfully logged out')
        return super().logout(request)

    def handle_no_permission(self):
        # If the user is not logged in, redirect to the login page
        return redirect(self.login_url)

class SubscribeView(View):
    template_name = 'userauths/subscribe.html'
    form_class = SubscribeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                Subscribers.objects.create(email=email)
                messages.success(request, "You're subscribed successfully")
                return render(request, self.template_name, {'email': email})
            except IntegrityError:
                # Set a custom error message for the email field
                form.add_error('email', 'This email is already subscribed.')
                messages.warning(request, "This email is already subscribed.")
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})
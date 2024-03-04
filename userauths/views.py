from typing import Any
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from .forms import RegistrationForm, LoginForm, SubscribeForm
from .models import FinanceUserRole, StockUserRole, Subscribers, CustomerUserRole, User, VendorUser
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'userauths/sign-up.html'
    model = CustomerUserRole
    form_class = RegistrationForm
    success_message = ' You have successfully registered.'
    redirect_authenticated_user=True
    success_url = reverse_lazy('core:index')


    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Authenticate the user using email and password
        user = self.object  # Newly created user instance
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')

        # Set the role of the user to "CUSTOMER"
        self.object.role = self.object.Role.CUSTOMER  # Adjust as per your model structure
        self.object.save()

        # Authenticate the user using email and password
        user = authenticate(self.request, username=email, password=form.cleaned_data.get('password1'))


        # Log in the authenticated user
        if user is not None:
            login(self.request, user)

        return response
class MyLoginView(SuccessMessageMixin,LoginView):
    template_name = 'userauths/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm
    success_message='Logged in Successfully!'

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'customeruserrole'):
            return reverse_lazy('core:index')
        elif hasattr(user, 'vendoruser'):
            return reverse_lazy('vendors:index')
        elif hasattr(user, 'financeuserrole'):
            return reverse_lazy('finance:dashboard')
        elif hasattr(user, 'stockuserrole'):
            return reverse_lazy('stock:dashboard')
        elif user.is_superuser:
            return reverse_lazy('admin_dashboard')
        else:
            return reverse_lazy('core:index') 


    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)
    
class MyLogoutView(LoginRequiredMixin, LogoutView):

    def get_success_url(self):
        # Redirect the user to the desired URL after logout
        return reverse_lazy('core:index')
    
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
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from userauths.models import VendorUser, User
from django.urls import reverse_lazy, reverse
from .forms import RegisterVendorForm, EditProfileForm
from core.models import Product, Feedback
from .forms import VendorFeedbackForm
from django.contrib import messages

# Create your views here.
class VendorHomeTemplateView(TemplateView):
    template_name = "vendors/vendor_home.html"

    def get_context_data(self, **kwargs) -> dict[str, ]:
        context = super().get_context_data(**kwargs)  
        vendor=get_object_or_404(VendorUser, email=self.request.user.email)
        context["vendor"] =vendor
    
        return context
    

class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'vendors/vendor_register.html'
    form_class = RegisterVendorForm
    success_message = 'You have successfully registered.'
    redirect_authenticated_user = True
    success_url = reverse_lazy('vendors:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Authenticate the user using email and password
        user = self.object  # Newly created user instance

        # Log in the authenticated user
        if user is not None:
            login(self.request, user)

        return response

class CatalogueListView(ListView):
    template_name='vendors/calatogue.html'
    model=Product

    def get_queryset(self):
        products = Product.objects.filter(vendor=self.request.user)
        return products
    
    def get_context_data(self, **kwargs) -> dict[str, ]:
        context = super().get_context_data(**kwargs)
        products= self.get_queryset()
        context["products"] = products
        return context
class EditProfileFormView(FormView):
    template_name='vendors/edit_profile.html'
    form_class=EditProfileForm
    success_message='You have updated profile successfully'
    success_url=reverse_lazy('vendors:index')

    def form_valid(self, form):
        profile=get_object_or_404(VendorUser, email=self.request.user.email)
        
        profile.image=form.cleaned_data['image']
        profile.phone=form.cleaned_data['phone']
        profile.bio=form.cleaned_data['bio']
        profile.description=form.cleaned_data['description']
        profile.city=form.cleaned_data['city']
        profile.vendor_address=form.cleaned_data['vendor_address']
        profile.business_email=form.cleaned_data['business_email']

        profile.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return self.success_url
    
class VendorFeedbackFormView(LoginRequiredMixin, FormView):
    template_name='vendors/vendor_feedback.html'
    form_class=VendorFeedbackForm
    model=Feedback

    def form_valid(self, form):
        if self.request.user.verified:
            user=self.request.user
            feedback=Feedback.objects.create(
                user=user,
                message=form.cleaned_data['message']
            )
            messages.success(self.request, 'Feedback submitted successfully.')
            return super().form_valid(form)
        else :
            messages.error(self.request, 'You need to be a verified user to submit feedback.')
            return redirect('vendors:index')
    def get_success_url(self) -> str:
        return reverse_lazy('vendors:index')
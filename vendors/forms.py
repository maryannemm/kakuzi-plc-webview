from django.contrib.auth.forms import UserCreationForm
from django import forms
from userauths.models import User, VendorUser
from django.core.validators import RegexValidator
from core.models import Feedback

class RegisterVendorForm(UserCreationForm):
        username= forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Username'}), label='Username')
        email= forms.EmailField( widget=forms.TextInput(attrs={'placeholder':'Email'}), label='Email')
        password1= forms.CharField( widget=forms.PasswordInput(attrs={'placeholder':'Password'}), label='Password')
        password2= forms.CharField( widget=forms.PasswordInput(attrs={'placeholder':' Confirm Password'}), label='Confirm Password')
        title = forms.CharField(max_length=100, label='Business Title')
        vendor_address = forms.CharField(max_length=100, label='Address')
        vendor_phone = forms.CharField(max_length=20, label='Phone')
        description = forms.CharField(widget=forms.Textarea, label='Description', required=False)
        city = forms.CharField(max_length=50, label='City', required=False)
        business_email = forms.EmailField(label='Business Email', required=False)


        class Meta:
            model =VendorUser
            fields = ['username', 'email', 'password1', 'password2', 'title', 'vendor_address', 'vendor_phone', 'description', 'city', 'business_email']

class EditProfileForm(forms.ModelForm):
      image=forms.ImageField(label='image')
      bio=forms.CharField(widget=forms.Textarea({'placeholder':'Your Bio'}))
      phone=forms.CharField(
        validators=[RegexValidator(r'^\d{10}$', 
        message="Phone number must be 10 digits")], 
        widget=forms.TextInput({'placeholder':'Phone Number'}))
      description=forms.CharField(widget=forms.Textarea({'placeholder':'Description'}))
      city=forms.CharField(widget=forms.TextInput({'placeholder':'city'}))
      business_email=forms.EmailField(widget=forms.EmailInput({'placeholder':'email'}))
      vendor_address=forms.CharField(widget=forms.TextInput({'placeholder':'Business Address'}))

      class Meta:
            model=VendorUser
            fields=['image','bio','phone','description','city', 'business_email', 'vendor_address']
            
class VendorFeedbackForm(forms.ModelForm):
    message=forms.CharField(widget=forms.TextInput({'placeholder':'Enter your feedback'}))
    class Meta:
        model=Feedback
        fields=['message']
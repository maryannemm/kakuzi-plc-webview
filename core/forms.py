from django import forms
from core.models import ProductReview, Address, ShippingCompany, ContactUs
from userauths.models import Profile
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
 
class ProductReviewForm(forms.ModelForm):
  review=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'write a review'}))

  class Meta:
    model=ProductReview
    fields=['review', 'ratings']

class CustomerAddressForm(forms.Form):
  first_name = forms.CharField(label='First Name', max_length=100, error_messages={'required': 'First name is required'})
  last_name = forms.CharField(label='Last Name', max_length=100, error_messages={'required': 'Last name is required'})
  address = forms.CharField(label='Address', max_length=255, error_messages={'required': 'Address is required'})
  phone = forms.CharField(
      label='Phone',
      max_length=10,
      min_length=10,
      validators=[RegexValidator(r'^\d{10}$', message="Phone number must be 10 digits")],
      error_messages={
          'required': 'Phone number is required',
          'min_length': 'Phone number must be 10 digits',
          'max_length': 'Phone number must be 10 digits',
          'invalid': 'Invalid phone number format. Please enter a 10-digit number.'
      }
  )
  city = forms.CharField(label='City', max_length=100, error_messages={'required': 'City is required'})
  county = forms.CharField(label='County', max_length=100, error_messages={'required': 'County is required'})
  country = forms.CharField(label='Country', max_length=100, error_messages={'required': 'Country is required'})

  class Meta:
        model = Address
        fields = '__all__'

class ShippingCompanyForm(forms.ModelForm):
    company_name = forms.ModelChoiceField(queryset=ShippingCompany.objects.all(), empty_label=None )

    class Meta:
        model = ShippingCompany
        fields = [ 'company_name']
        error_messages = {'company_name': {'required': 'Shipping company selection is required'}}

class ContactUsForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Name'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    subject=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Subject'}))
    message=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write your message'}))
    def __init__(self, *args, **kwargs):
        super(ContactUsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = '' 
    class Meta:
        model=ContactUs
        fields='__all__'
    
class EditCustomerProfileForm(forms.ModelForm):
    image=forms.ImageField()
    full_name=forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':' Full Name'}))
    bio=forms.CharField(widget=forms.Textarea({'class':'form-group','placeholder':'Enter Bio '}))

    class Meta:
        model=Profile
        fields=['image', 'full_name', 'bio']
        
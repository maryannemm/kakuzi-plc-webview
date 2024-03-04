from django import forms
from userauths.models import StockUserRole
from django.core.validators import RegexValidator

class CreateProductForm(forms.ModelForm):
    image=forms.ImageField(label='image')
    bio=forms.CharField(widget=forms.Textarea({'placeholder':'Your Bio'}))
    phone=forms.CharField(
        validators=[RegexValidator(r'^\d{10}$', 
        message="Phone number must be 10 digits")], 
        widget=forms.TextInput({'placeholder':'Phone Number'}))
    full_name=forms.CharField(widget=forms.TextInput({'placeholder':'Full Name'}))
    first_name=forms.CharField(widget=forms.TextInput({'placeholder':'First Name'}))
    last_name=forms.CharField(widget=forms.TextInput({'placeholder':'Last Name'}))

    class Meta:
        model=StockUserRole
        fields=['image', 'phone', 'bio','full_name', 'first_name', 'last_name']
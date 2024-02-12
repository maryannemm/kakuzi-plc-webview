from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from userauths.models import User, Subscribers

class RegistrationForm(UserCreationForm):
    username= forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email= forms.EmailField( widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password1= forms.CharField( widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2= forms.CharField( widget=forms.PasswordInput(attrs={'placeholder':' Confirm Password'}))

    class Meta:
        model =User
        fields= ['username', 'email']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        label="Email",  # You can customize the label as well
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password",  # You can customize the label as well
    )

    class Meta:
        model = User
        fields = ['username', 'password']

class SubscribeForm(forms.Form):
    email= forms.EmailField( widget=forms.TextInput(attrs={'placeholder':'Email'}))
    

    class Meta:
        model=Subscribers
        fields=['email']
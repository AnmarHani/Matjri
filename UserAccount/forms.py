from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from django import forms


class LoginForm(forms.Form):
    username= forms.CharField(max_length=100)
    password= forms.CharField(widget=forms.PasswordInput())

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ProfileForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)
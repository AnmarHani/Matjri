from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from django import forms

class ProductForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)
    stock = forms.IntegerField()
    price = forms.DecimalField(max_digits=5, decimal_places=2)
    location = forms.CharField(max_length=100)
    payment_type = forms.CharField(max_length=100)
    delivery_type = forms.CharField(max_length=100)
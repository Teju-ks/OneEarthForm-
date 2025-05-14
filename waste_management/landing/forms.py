from django import forms
from .models import Buyer, Seller, OrganicProduct, OrganicManure

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    city = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')])

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Buyer.objects.filter(username=username).exists() or Seller.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        if not cleaned_data.get('city'):
            raise forms.ValidationError('City is required')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')])

class OrganicProductForm(forms.ModelForm):
    class Meta:
        model = OrganicProduct
        fields = ['name', 'description', 'price', 'stock']  # Include only these fields


class OrganicManureForm(forms.ModelForm):
    class Meta:
        model = OrganicManure
        fields = ['name', 'description', 'price', 'stock']  # Include only these fields
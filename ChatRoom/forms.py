from django import forms
from django.utils.translation import ugettext_lazy as _

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control","placeholder": "Username"}))
    emailaddress = forms.EmailField(widget=forms.EmailInput(attrs={"class" : "form-control","placeholder": "Email Address"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class" : "form-control","placeholder": "Password"}))
    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={"class" : "form-control","placeholder": "Confirm Password"}))


from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
        email = forms.EmailField(required=True)
        first_name = forms.CharField(required=True)
        last_name = forms.CharField(required=True)
        middle_name = forms.CharField(required=False)
        
        class Meta:
                model = User
                fields = ["username", "first_name", "middle_name", "last_name", "email", "password1", "password2"]

class UserUpdateForm(forms.ModelForm):
        email = forms.EmailField(required=True)
        
        class Meta:
                model = User
                fields = ["username", "email"]
                
class ProfileUpdateForm(forms.ModelForm):
        class Meta:
                model = Profile
                fields = ["image"]
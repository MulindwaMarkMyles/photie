from django import forms
from django.contrib.auth.models import User
from .models import Profile, AccessLink
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
                
class SharePostsForm(forms.ModelForm):
        username = forms.CharField(widget=forms.TextInput(attrs={"readonly":"readonly"}))
        class Meta:
                model = AccessLink
                fields = ["username", "name", "email", "access_token"]
                
class AccessLinkLoginForm(forms.Form):
        email = forms.EmailField(required=True)
        access_token = forms.UUIDField(required=True)

                
                
                
                
                
        
                
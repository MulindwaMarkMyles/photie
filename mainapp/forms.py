from django import forms
from .models import Post

#not using it.
class FileForm(forms.ModelForm):
        class Meta:
                model = Post
                fields = ["context", "post"]
                
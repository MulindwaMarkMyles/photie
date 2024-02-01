from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

def validate_file_extensions(value):
        valid_extensions = ["jpg", "jpeg","png", "gif", "mp4", "avi", "mkv"]
        extension = value.name.split('.')[-1].lower()
        
        if extension not in valid_extensions:
                raise ValidationError(f"Unsupported file type, please upload only files with: {', '.join(map(str, valid_extensions))}.")
        
class Post(models.Model):
        context = models.TextField(blank=True)
        post = models.FileField(upload_to='images', validators=[validate_file_extensions])
        date_posted = models.DateTimeField(default=timezone.now)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        file_type = models.CharField(default="image", max_length=50)
        
        def __str__(self):
                return f"Post Info: {self.post.name}."
        
        def get_absolute_url(self):
                return reverse('home_page')
        
        def save(self, *args, **kwargs):
                # if not self.pk: can be used to prevent editing if  not in the creation instance
                file_extension = self.post.name.split('.')[-1].lower()
                if file_extension in ["jpg", "jpeg", "png"]:
                        self.file_type = 'image'
                elif file_extension in ["gif", "mp4", "avi", "mkv"]:
                        self.file_type = 'video'

                super().save(*args, **kwargs)
        


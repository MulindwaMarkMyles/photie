from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
        context = models.TextField(blank=True)
        post = models.ImageField(upload_to='images')
        date_posted = models.DateTimeField(default=timezone.now)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        
        def __str__(self):
                return f"Post Info: {self.post.name}."
        
        def get_absolute_url(self):
                return reverse('home_page')
        

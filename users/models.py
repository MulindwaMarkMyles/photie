from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# from mainapp.models import Post

class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        image = models.ImageField(default="default.png", upload_to="profile_pics")
        
        def __str__(self):
                return f"{self.user.username} Profile."
        
        def save(self, *args, **kwargs):
                super(Profile, self).save(*args, **kwargs)
                img = Image.open(self.image.path)
                
                if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        img.save(self.image.path)
                        
class AccessLink(models.Model):
        access_token = models.UUIDField(blank=False,editable=True)
        username = models.CharField(editable=True,blank=False,max_length=50,default="username")
        email = models.CharField(max_length=100,blank=False,default="email")
        name = models.CharField(blank=False,max_length=100,default="name")
        created_at = models.DateTimeField(auto_now_add=True)
        
        
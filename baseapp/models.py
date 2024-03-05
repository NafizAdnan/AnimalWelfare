from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
# Create your models here.
"""
class CustomUser(User):
    contact = models.CharField(max_length=20)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20)
"""
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    picture = models.ImageField(upload_to='post_pictures/', null=True, blank=True) 
    contact_info = models.CharField(max_length=100, null=True, blank=True)  
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.picture:
            img = Image.open(self.picture.path)

            # Resize the image
            max_size = (150,150)  # Define your desired maximum size here
            img.thumbnail(max_size)
            img.save(self.picture.path)

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('animal-detail',args=(str(self.id)))

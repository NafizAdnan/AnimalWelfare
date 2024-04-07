from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager, AbstractBaseUser
from PIL import Image
from django.urls import reverse
from datetime import date
from django.conf import settings
from django.core.validators import FileExtensionValidator


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.username, filename)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        # user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    password = models.CharField(max_length=25)
    email = models.EmailField(verbose_name='email', max_length=60)
    contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    dob = models.DateField(default=None, null=True, blank=True)
    preferences = []
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    friends = models.ManyToManyField("User",blank=True)

    def calculate_age(self):
        if not self.dob:
            return None
        today = date.today()
        age = today.year - self.dob.year

        if today.month < self.dob.month or (today.month == self.dob.month and today.day < self.dob.day):
            age -= 1

        return age
    age = property(calculate_age)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_picture:
            img = Image.open(self.profile_picture.path)

            # Resize the image
            max_size = (150,150)
            img.thumbnail(max_size)
            img.save(self.profile_picture.path)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']
    objects = UserManager()
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('user-detail',args=(str(self.username)))
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
class Animal(models.Model):
    title = models.CharField(max_length=20)
    age = models.IntegerField()
    breed = models.CharField(max_length=20)
    description = models.TextField()
    picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    vaccinated = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    available_for = models.CharField(max_length=20, default='adoption')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.picture:
            img = Image.open(self.picture.path)

            # Resize the image
            max_size = (150,150)
            img.thumbnail(max_size)
            img.save(self.picture.path)
    
    def get_absolute_url(self):
        return reverse('animal-detail',args=(str(self.id)))

class Accessories(models.Model):
    type = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    description = models.TextField()
    picture = models.ImageField(upload_to='accessory_pictures/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_by_identifier = models.CharField(max_length=100, null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    stock = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.picture:
            img = Image.open(self.picture.path)

            # Resize the image
            max_size = (150,150)
            img.thumbnail(max_size)
            img.save(self.picture.path)
    
    def get_absolute_url(self):
        return reverse('accessory-detail',args=(str(self.id)))
    
class Support(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)


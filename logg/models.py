from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import default


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, position, password=None):
        if not username:
            raise ValueError('Must have a username')
        if not position:
            raise ValueError('Must have an position')
        user = self.model(
            username=username,
            position = position,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, position, password):
        if not username:
            raise ValueError('Must have a username')
        if not position:
            raise ValueError('Must have an email address')
        user = self.create_user(
            username,
            position
        )
        user.is_admin = True
        user.is_staff = True;
        user.is_active = True;
        user.is_superuser = True;
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)
    position = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = False

    def has_module_perms(self, *args, **kwargs):
        return True

    def has_perm(self, *args, **kwargs):
        return True

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password','position']

    def __str__(self):
        return self.username+" "+self.position

class Advertisement(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='advertisements',default=True)
    thumbnail = models.ImageField(upload_to='advertisement/', default='product.svg')
    category = models.CharField(max_length=128,default='')
    sns = models.CharField(max_length=128,default='')
    title = models.CharField(max_length=128)
    product_name = models.CharField(max_length=128)
    description = models.TextField(default='description of the product')
    min_budget = models.PositiveIntegerField(default=0)
    max_budget = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to='advertisement/', default='product.svg')

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    img = models.ImageField(upload_to='profile/', default='product.svg')
    platform = models.CharField(max_length=128,default='')
    content = models.CharField(max_length=128,default='')
    min_budget = models.PositiveIntegerField(default=0)
    max_budget = models.PositiveIntegerField(default=0)
    urls = models.CharField(max_length=100, default='')
    text_box = models.CharField(max_length=512,default='')








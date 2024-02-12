from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

#superuser
class User(AbstractUser):
    email= models.EmailField(unique= True)
    username =models.CharField(max_length=100)
    bio= models.CharField(max_length=400, default='My Bio')
    #use the email filed in admin login instead of username
    USERNAME_FIELD='email'
    REQUIRED_FIELDS= ['username']

    def __str__(self):
        return self.username
class Subscribers(models.Model):
    email= models.EmailField(unique= True)

    class Meta:
        verbose_name_plural = 'Subscribers'
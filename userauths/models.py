from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.hashers import make_password

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)  

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=400, default='My Bio', null=True)
    full_name = models.CharField(max_length=60, default=None, null=True)
    verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, null=True, blank=True, default=None)
    image = models.ImageField(upload_to='image', default='https://i0.wp.com/digitalhealthskills.com/wp-content/uploads/2022/11/3da39-no-user-image-icon-27.png?fit=500%2C500&ssl=1')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class CustomerUserRole(User):
    pass

    class Meta:
        verbose_name_plural = 'Customers'

class VendorUser(User):  
    title = models.CharField(max_length=100, default='farmer business')
    vendor_address = models.CharField(max_length=100, default='123, main street, nairobi')
    description = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    business_email = models.EmailField(null=True, blank=True)
    country=models.CharField(max_length=30, default='Kenya')

    class Meta:
        verbose_name_plural = 'Farmers'

class FinanceUserRole(User):
    #has password
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Financial Managers'

class StockUserRole(User):

    #hash the password
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Stock Managers'

class Subscribers(models.Model):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name_plural = 'Subscribers'

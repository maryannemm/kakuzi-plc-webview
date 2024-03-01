from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from shortuuidfield import ShortUUIDField 

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)  

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=400, default='My Bio', null=True)
    full_name = models.CharField(max_length=60, default=None, null=True)
    verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, null=True, blank=True, default=None)
    image = models.ImageField(upload_to='image', default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'
        VENDOR = 'VENDOR', 'Farmer'
        FINANCE = 'FINANCE', 'Finance'
        STOCK = 'STOCK', 'Stock'

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
    pass

    class Meta:
        verbose_name_plural = 'Financial Managers'

class StockUserRole(User):
    pass

    class Meta:
        verbose_name_plural = 'Stock Managers'

class Subscribers(models.Model):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name_plural = 'Subscribers'

from django.db import models
from shortuuid.django_fields import ShortUUIDField  # Correct import statement
from django.utils.html import mark_safe
from userauths.models import User
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

STATUS_CHOICES = (
    ("pending", "Pending"),
    ("shipped", "Shipped"),
    ("completed", "Completed"),
  
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("in_review", "In Review"),
    ("delivered", "Delivered"),
    ("published", "Published"),
)
RATINGS = (
    ( 1,"★☆☆☆☆"),
    ( 2,"★★☆☆☆"),
    ( 3,"★★★☆☆"),
    ( 4,"★★★★☆"),
    ( 5,"★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)  

class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=30, prefix='cat', alphabet='abcdefghij12345') 
    title = models.CharField(max_length=100, default='fruit')
    image = models.ImageField(upload_to='category', default='category.jpg')

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" />' % self.image.url)  

    def __str__(self):
        return self.title

class Supplier(models.Model):
    vid = ShortUUIDField(unique=True, max_length=31, prefix='supplier', alphabet='abcdefghij12345') 
    title = models.CharField(max_length=100, default='farmer business')
    image = models.ImageField(upload_to=user_directory_path, default='farmer.jpg')
    address = models.CharField(max_length=100, default='123, main street, nairobi', unique=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True, default='+2544567890')
    description = RichTextUploadingField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    city = models.CharField(max_length=50, null=True, blank=True)
    business_email = models.EmailField(null=True, blank=True)
 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Farmers"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" />' % self.image.url)  

    def __str__(self):
        return self.title

  


class Product(models.Model):
    pid = ShortUUIDField(unique=True, max_length=30, alphabet='abcdefghij12345')
    title = models.CharField(max_length=100, default='vegetable')
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = RichTextUploadingField(null=True, blank=True, default='this is the product')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.0)
    quantity_available = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    product_status = models.CharField(choices=STATUS, max_length=50)
    featured = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    life=models.CharField(max_length=50, default='10')
    mfd=models.DateTimeField(auto_now_add=False, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True,default='')
    user_reviewed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug based on the title
            self.slug = slugify(self.title)
            # Ensure the generated slug is unique
            self.unique_slug()
        super().save(*args, **kwargs)

    def unique_slug(self):
        """
        Ensure the generated slug is unique by appending a number if necessary.
        """
        counter = 1
        original_slug = self.slug
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" />' % self.image.url)

    def __str__(self):
        return self.title
    

class ProductImages(models.Model):
    images= models.ImageField(upload_to='product-images', default='product.jpg')
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null = True)
    date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural=" Product Images"


##############################cart, orders, ordered items in the cart
class CartOrder(models.Model):
    #user wo adds items to their cart
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.0)
    payment_status=models.BooleanField(default=False)
    order_date=models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='pending')

    class Meta:
        verbose_name_plural='Cart Orders'


class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_number=models.CharField(max_length=200)
    item=models.CharField(max_length=200)
    image=models.ImageField(max_length=200)
    price=models.DecimalField(max_digits=200, default=200, decimal_places=2)
    total=models.DecimalField(max_digits=200, default=200, decimal_places=2)
    qty=models.IntegerField(default=1)

    class Meta:
        verbose_name_plural='Cart Order Items'

    def category_image(self):
        return mark_safe('<img src="%s" width="50" />' % self.image.url)  
    
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" />' % self.image.url)
    
    ##########product Review, wishlist address############################

class ProductReview(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null= True)
    review=models.TextField()
    ratings=models.IntegerField(choices=RATINGS, default=None)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title
    def get_rating(self):
        return self.ratings

class WishList(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null= True)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "WishList"

    def __str__(self):
        return self.product.title
    def get_rating(self):
        return self.ratings
    

class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    address=models.CharField(max_length=100, null=True)
    status= models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

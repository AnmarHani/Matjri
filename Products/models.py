from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import FloatField

# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", verbose_name="seller_products")
    image = models.ImageField(default="product.png", upload_to="images", blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    location = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=100)
    delivery_type = models.CharField(max_length=100)
    likes = models.ManyToManyField(User, null=True, blank=True, related_name='likes')
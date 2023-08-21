from django.db import models
from taggit.managers import TaggableManager
from django.db.models import Avg

from apps.user.models import Customer


class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=1024)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.CASCADE)
    pid=models.CharField(max_length=32, unique=True, null=False, blank=False)
    description = models.TextField()
    retail_price = models.FloatField()
    product_url = models.TextField(null=True)
    tags = TaggableManager()
    brand = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.product_name}({self.id})"



class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, related_name='customers', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlist_product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} wishlist {self.product}"

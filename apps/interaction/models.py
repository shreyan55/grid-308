from django.db import models
from django.core.exceptions import ValidationError

from apps.user.models import Customer
from apps.product.models import Product

class Interaction(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    InteractionChoices = [
        ('click','Click'),
        ('wishlist','Wishlist'),
        ('cart','Cart'),
        ('order','Order'),
        ('rating','Rating')
    ]
    interaction = models.CharField(max_length=20,choices=InteractionChoices)
    rating = models.IntegerField(blank=True,null=True)
    
    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')
    

class Result(models.Model):
    data=models.JSONField()
    timestamp=models.DateTimeField(auto_now=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.timestamp)
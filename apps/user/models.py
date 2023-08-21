from django.db import models
from django.core.exceptions import ValidationError


class Customer(models.Model):
    Gender = [
        ('M','Male'),
        ('F','Female'),
    ] 
    email=models.EmailField(unique=True,max_length=64)
    first_name=models.CharField(max_length=64)
    last_name=models.CharField(max_length=64)
    age=models.IntegerField(default=0,null=True,blank=True)
    gender=models.CharField(max_length=1,choices=Gender,default='P')
    intrest=models.CharField(max_length=64,null=True,blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)    
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.PositiveIntegerField(help_text="Enter 6-digit PIN code")

    def clean(self):
        if len(str(self.pincode)) != 6:
            raise ValidationError({'pincode': 'PIN code must be 6 digits long.'})

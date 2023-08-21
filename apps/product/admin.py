from django.contrib import admin

from .models import Product, Category, Wishlist

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Wishlist)

# Register your models here.

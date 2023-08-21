import csv
from django.core.files import File
from  apps.product.models import Product, Category  # Import your models here

def import_data_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:   
            category_name = row['product_category_tree'].split(' >> ')[0].strip()
            category, created = Category.objects.get_or_create(name=category_name)
            
            product = Product(
                product_name=row['product_name'],
                category=category,
                description=row['description'],
                retail_price=float(row['retail_price']),
                brand=row['brand']
            )
            
            # Assuming you want to upload product_picture as well
            # You need to set up proper MEDIA_ROOT and MEDIA_URL in your settings
            
            product.save()



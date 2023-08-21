import csv, os
from django.core.management.base import BaseCommand
from apps.product.models import Category, Product

class Command(BaseCommand):
    help = 'Populate products and categories from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        csv_file = os.path.join(os.getcwd(),csv_file)
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category_name = row['product_category_tree'].split('>>')[0].strip()
                product_name = row['product_name']
                pid = row['pid']
                try:
                    retail_price = float(row['retail_price'])
                except:
                    retail_price =0.0
                product_url = row['product_url']
                description = row['description']
                brand = row['brand']
                try:
                    category, created = Category.objects.get_or_create(category_name=category_name)
                    product, created = Product.objects.get_or_create(
                        product_name=product_name,
                        category=category,
                        pid=pid,
                        retail_price=retail_price,
                        product_url=product_url,
                        description=description,
                        brand=brand,
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error created product: {product}'))
                    self.stdout.write(self.style.ERROR(f'Exception {e}'))
                self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product}'))

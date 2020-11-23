import csv
from inventario_app.models import Product

def run():
    with open('/Users/rjnocelli/Desktop/dev/django/django_projects/ecommerce/scripts/product_data.csv', 'r') as csv_file:
        f = csv.reader(csv_file, delimiter=',')
        
        for product in f:
            name = product[0]
            price = int(f"{product[1]}")
            description = product[2]
            p = Product.objects.get_or_create(name=name, price=price, description=description)
            print(f"product {p[0].name} created")
            

    

import csv
import random
from faker import Faker

fake = Faker()

# Number of entries
num_entries = 1000

# CSV filename
csv_file_name = 'product.csv'

# Fields
field_names = ['name', 'price', 'description', 'category', 'image']

# Categories
categories = [
    'Electronics', 'Clothing', 'Home & Garden', 'Toys',
    'Sports & Outdoors', 'Books', 'Beauty & Personal Care',
    'Automotive', 'Health & Household', 'Pet Supplies'
]

with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for i in range(num_entries):
        entry = {
            'name': fake.catch_phrase(),  # random realistic product-like name
            'price': round(random.uniform(10.0, 1000.0), 2),
            'description': fake.text(max_nb_chars=100),  # short fake description
            'category': random.choice(categories),
            'image': f'image{i+1}.jpg'
        }
        writer.writerow(entry)

print(f'Supabase CSV file \"{csv_file_name}\" has been generated with {num_entries} entries.')

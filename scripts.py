import csv
import random
from faker import Faker

fake = Faker()

# Number of entries
num_entries = 1000

# CSV filename
csv_file_name = 'posts.csv'

# Fields
field_names = ['title', 'content', 'published']


with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    
    for i in range(num_entries):
        entry = {
            'title': fake.catch_phrase(),  # random realistic product-like name
            'content': fake.text(max_nb_chars=100),  # short fake description
            'published': fake.boolean()
        }
        writer.writerow(entry)

print(f'Supabase CSV file \"{csv_file_name}\" has been generated with {num_entries} entries.')

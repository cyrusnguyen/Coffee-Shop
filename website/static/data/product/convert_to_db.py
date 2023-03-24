import json
import sqlite3
import os

product_dir = 'C:/Users/Cyrus/Documents/Project/coffee-shop/website/static/data/product/'
db_path = 'C:/Users/Cyrus/Documents/Project/coffee-shop/website/static/data/product/' + 'file.db'
cat_dir = 'C:/Users/Cyrus/Documents/Project/coffee-shop/website/static/data/category/'

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS categories
               (category_id INTEGER PRIMARY KEY, name TEXT, description TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS products
               (product_id INTEGER PRIMARY KEY, name TEXT, price DOUBLE, description TEXT, image TEXT, category_id INTEGER, FOREIGN KEY (category_id) REFERENCES categories(category_id))''')

# Insert data from multiple JSON files to categories
for filename in os.listdir(cat_dir):
    if filename.endswith('.json'):
        
        with open(os.path.join(cat_dir, filename), 'r') as f:
            data = json.load(f)
            category_id = data["Category_ID"]
            name = data["Name"]
            description = data["Description"]

            cur.execute('INSERT INTO categories (category_id, name, description) VALUES (?, ?, ?)', (category_id, name, description))

# Insert data from multiple JSON files to categories
for filename in os.listdir(product_dir):
    if filename.endswith('.json'):
        
        with open(os.path.join(product_dir, filename), 'r') as f:
            data = json.load(f)
            product_id = data["Product_ID"]
            name = data["Name"]
            price = data["Price"]
            description = data["Description"]
            image = data["Image"]
            category_id = data["Category_ID"]
            cur.execute('INSERT INTO products (product_id, name, price, description, image, category_id) VALUES (?, ?, ?, ?, ?, ?)', (product_id, name, price, description, image, category_id))

# Commit changes and close connection
conn.commit()
conn.close()    

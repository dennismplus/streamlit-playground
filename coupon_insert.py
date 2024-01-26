import sqlite3
import random
import string

# Connect to the SQLite database (change the database name as needed)
conn = sqlite3.connect('streamlit.db')
cursor = conn.cursor()

# Define the number of coupons to insert
num_coupons = 100

# Insert 100 coupon records
for i in range(1, num_coupons + 1):
    coupon_id = i
    user_id = random.randint(1, 20)  # Assuming you have 20 users
    product_id = random.randint(1, 20)  # Assuming you have 20 products
    coupon_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    discount = round(random.uniform(5, 50), 2)
    expiration_date = f'2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'  # Random expiration date
    is_active = random.choice([True, False])
    is_canceled = random.choice([True, False])
    is_timed_out = random.choice([True, False])

    cursor.execute("""
        INSERT INTO Coupons (coupon_id, user_id, product_id, coupon_code, discount, expiration_date, is_active, is_canceled, is_timed_out)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (coupon_id, user_id, product_id, coupon_code, discount, expiration_date, is_active, is_canceled, is_timed_out))

# Commit the changes and close the database connection
conn.commit()
conn.close()

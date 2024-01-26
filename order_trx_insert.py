import sqlite3
import random

# Connect to the SQLite database (change the database name as needed)
conn = sqlite3.connect('streamlit.db')
cursor = conn.cursor()

# Define the number of order and transaction records to insert
num_records = 50

# Insert 50 sample order and transaction records
for i in range(1, num_records + 1):
    order_id = i
    user_id = random.randint(1, 20)  # Assuming you have 20 users
    product_id = random.randint(1, 20)  # Assuming you have 20 products
    total_amount = round(random.uniform(10, 200), 2)
    order_date = f'2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'  # Random order date

    # Simulate the use of coupons or rewards in transactions
    use_coupon = random.choice([True, False])
    use_reward = random.choice([True, False])
    coupon_id = None
    reward_id = None

    if use_coupon:
        coupon_id = random.randint(1, 100)  # Assuming you have 100 coupons

    if use_reward:
        reward_id = random.randint(1, 100)  # Assuming you have 100 rewards

    cursor.execute("""
        INSERT INTO Orders (order_id, user_id, product_id, total_amount, order_date)
        VALUES (?, ?, ?, ?, ?)
    """, (order_id, user_id, product_id, total_amount, order_date))

    cursor.execute("""
        INSERT INTO Transactions (transaction_id, user_id, transaction_type, amount, transaction_date, order_id, coupon_id, reward_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (i, user_id, 'Purchase', total_amount, order_date, order_id, coupon_id, reward_id))

# Commit the changes and close the database connection
conn.commit()
conn.close()

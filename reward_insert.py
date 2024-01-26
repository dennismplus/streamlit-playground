import sqlite3
import random
import string

# Connect to the SQLite database (change the database name as needed)
conn = sqlite3.connect('streamlit.db')
cursor = conn.cursor()

# Define the number of rewards to insert
num_rewards = 100

# Insert 100 reward records
for reward_id in range(1, num_rewards + 1):
    user_id = random.randint(1, 20)  # Assuming you have 20 users
    reward_type = 'Reward Type' + str(reward_id)
    reward_points = random.randint(1, 100)
    date_earned = f'2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'  # Random date earned

    cursor.execute("""
        INSERT INTO Rewards (reward_id, user_id, reward_type, reward_points, date_earned)
        VALUES (?, ?, ?, ?, ?)
    """, (reward_id, user_id, reward_type, reward_points, date_earned))

# Commit the changes and close the database connection
conn.commit()
conn.close()

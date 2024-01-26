import psycopg2
import random
from datetime import date, timedelta

conn_string = "postgres://dennis:0M7vglpmoFCE@ep-calm-star-072623.ap-southeast-1.aws.neon.tech/cdm?sslmode=require"


# Function to generate random coupon code
def generate_coupon_code():
    prefix = "COUPON"
    suffix = str(random.randint(1000, 9999))
    return f"{prefix}{suffix}"


# Function to generate random expiration date
def generate_expiration_date():
    today = date.today()
    days_until_expiration = random.randint(1, 365)
    expiration_date = today + timedelta(days=days_until_expiration)
    return expiration_date


# Function to insert 100 coupon records
def insert_coupons():
    try:
        # Establish a database connection
        # conn = psycopg2.connect(host="192.168.1.3",
        #                         port="5432",
        #                         user="postgres",
        #                         password="password",
        #                         database="cdm",
        #                         options="-c search_path=dbo,streamlit")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        # Insert 100 coupon records
        for _ in range(100):
            user_id = random.randint(1, 20)  # Assuming you have 20 users in your Users table
            product_id = random.randint(1, 20)  # Assuming you have 20 products in your Products table
            coupon_code = generate_coupon_code()
            discount = round(random.uniform(5, 50), 2)
            expiration_date = generate_expiration_date()
            is_active = random.choice([True, False])
            is_canceled = random.choice([True, False])
            is_timed_out = random.choice([True, False])

            cursor.execute(
                """
                INSERT INTO Coupons (user_id, product_id, coupon_code, discount, expiration_date, is_active, is_canceled, is_timed_out)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    product_id,
                    coupon_code,
                    discount,
                    expiration_date,
                    is_active,
                    is_canceled,
                    is_timed_out,
                ),
            )

        # Commit the changes and close the connection
        conn.commit()
        print("Inserted 100 coupon records successfully!")

    except (Exception, psycopg2.Error) as error:
        print(f"Error inserting coupon records: {error}")

    finally:
        if cursor:
            cursor.close()
            conn.close()


# Call the insert_coupons function to insert records
insert_coupons()

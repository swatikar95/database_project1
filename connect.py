#importing necessary modules
import mysql.connector
import hashlib

# function using SHA-256
def hash_string(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

# connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="*****", #hide the pass for security
    database="users"
)
cursor = conn.cursor()

cursor.execute("create table users (email_hash VARCHAR(255), password_hash VARCHAR(255))")

with open('credentials1.txt','r') as file:
    for line in file:
        parts = line.strip().split(":", maxsplit=1)  # split at most 2 parts
        if len(parts) == 2:  # ensures exactly 2 parts
            email, password = parts  # unpacking
            email_hash = hash_string(email)
            password_hash = hash_string(password)
        else:
            print(f"Skipping invalid line: {line.strip()}")

        cursor.execute("insert into users (email_hash, password_hash) VALUES (%s, %s)", (email_hash, password_hash))

# commit and close connection
conn.commit()
cursor.close()
conn.close()

with open('credentials2.txt','r') as file:
    for line in file:
        parts = line.strip().split(":", maxsplit=1)
        if len(parts) == 2:
            email, password = parts
            email_hash = hash_string(email)
            password_hash = hash_string(password)
        else:
            print(f"Skipping invalid line: {line.strip()}")

        cursor.execute("insert into users (email_hash, password_hash) VALUES (%s, %s)", (email_hash, password_hash))


conn.commit()
cursor.close()
conn.close()
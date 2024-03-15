from flask import Flask, request, render_template
import mysql.connector
import hashlib
import time

app = Flask(__name__)

# function to hash strings
def hash_string(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def web_ui():
    message = ""
    query_time = 0

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        email_hash = hash_string(email)
        password_hash = hash_string(password)

        #connect to database
        conn = mysql.connector.connect(host='localhost', user='root', password='****', database="users")

        # #start timer
        start_time = time.time()

        #first checks if email exists
        with conn.cursor(buffered=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE email_hash=%s", (email_hash,))
            email_result = cursor.fetchone()
            # helps to consume all results
            while cursor.nextset(): 
                pass  
        
        #if email exists, then checks if email and password exits
        if email_result:
            with conn.cursor(buffered=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE email_hash=%s AND password_hash=%s", (email_hash, password_hash))
                password_result = cursor.fetchone()
                # helps to consume all results
                while cursor.nextset(): 
                    pass  

            # end timer
            end_time = time.time()
            query_time = end_time - start_time

            if password_result:
                message = f'Credentials Matched! Query took {query_time:.3f} seconds.'
            else:
                message = f'Email found, but the password is incorrect. Query took {query_time:.3f} seconds.'
        else:
            # end timer
            end_time = time.time()
            query_time = end_time - start_time

            message = f'Email does not exist in the database. Query took {query_time:.3f} seconds.'

        conn.commit()  
        conn.close()

    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)

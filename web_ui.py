from flask import Flask, request,render_template
import mysql.connector
import hashlib

app = Flask(__name__)

# function to hash strings
def hash_string(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

@app.route('/',methods=['GET','POST'])
def web_ui():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        email_hash = hash_string(email)
        password_hash = hash_string(password)

        #connect to database
        conn = mysql.connector.connect(host='localhost', user='root', password='amiParbo54#', database="users")
        cursor = conn.cursor()

        #check if the email and pass exist in the database
        cursor.execute("select * from users where email_hash=%s AND password_hash=%s",(email_hash,password_hash))
        result = cursor.fetchone()

        if result:
            return render_template('index.html',message='Credentials Matched!')
        else:
            return render_template('index.html',message='Credentials NOT exist!!')
        
    return render_template('index.html',message="")

if __name__ == '__main__':
    app.run(debug=True)
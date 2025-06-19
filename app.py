from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv,find_dotenv
import os

_ = load_dotenv(find_dotenv())

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')

mysql = MySQL(app)

#Home route
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test-db")
def test_db():
    try:
        cur = mysql.connect.cursor()
        cur.execute("SELECT 1")
        return "Databse connected succesfully"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

@app.route("/contacts")
def contacts():
    cur = mysql.connect.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    cur.close()
    return render_template("contacts.html",contacts=data)

@app.route("/add-contact",methods=['GET','POST'])
def add_contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connect.cursor()
        cur.execute("INSERT INTO contacts (name,email,phone) VALUES (%s,%s,%s)", (name,email,phone))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('contacts'))
    
    return render_template("add_contact.html")


if __name__ == "__main__":
    app.run(debug=True)
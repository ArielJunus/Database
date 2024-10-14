from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password132'
app.config['MYSQL_DB'] = 'address'

# Initialize the MySQL connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Create the 'addresses' table if it doesn't exist
def create_table():
    connection = get_db_connection()
    if connection is None:
        print("Failed to create table because connection is None")
        return
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            address VARCHAR(255)
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

@app.route('/')
def index():
    # Fetch all addresses from the database
    connection = get_db_connection()
    if connection is None:
        return "Database connection failed!"
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM addresses')
    addresses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', addresses=addresses)

@app.route('/add', methods=['POST'])
def add_address():
    # Get form data
    name = request.form['name']
    address = request.form['address']
    
    # Insert the new address into the database
    connection = get_db_connection()
    if connection is None:
        return "Database connection failed!"
    cursor = connection.cursor()
    cursor.execute('INSERT INTO addresses (name, address) VALUES (%s, %s)', (name, address))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect('/')

if __name__ == '__main__':
    create_table()  # Create the table when starting the app
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from join import init_db, get_contacts, add_contact, edit_contact, delete_contact, get_contact_by_id

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password132'
app.config['MYSQL_DB'] = 'databook1'

mysql = init_db(app)

@app.route('/')
def index():
    contacts = get_contacts(mysql)
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact_route():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        group_name = request.form['group_name']
        add_contact(mysql, name, phone, email, group_name)
        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact_route(id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        group_name = request.form['group_name']
        edit_contact(mysql, id, name, phone, email, group_name)
        return redirect(url_for('index'))

    contact = get_contact_by_id(mysql, id)  # Fetching a single contact by ID
    if contact:
        return render_template('edit.html', contact=contact)
    else:
        return "Contact not found", 404

@app.route('/delete/<int:id>', methods=['GET'])
def delete_contact_route(id):
    delete_contact(mysql, id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)












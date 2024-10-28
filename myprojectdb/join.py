from flask_mysqldb import MySQL

def init_db(app):
    mysql = MySQL(app)
    return mysql

def get_contacts(mysql):
    cur = mysql.connection.cursor()
    # Join contacts with phone_info and email_info to fetch all details
    cur.execute("""
        SELECT contacts.id, contacts.name, phone_info.phone, email_info.email, contacts.group_name
        FROM contacts
        LEFT JOIN phone_info ON contacts.id = phone_info.contact_id
        LEFT JOIN email_info ON contacts.id = email_info.contact_id
    """)
    contacts = cur.fetchall()
    cur.close()
    return contacts

def get_contact_by_id(mysql, id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT contacts.id, contacts.name, phone_info.phone, email_info.email, contacts.group_name
        FROM contacts
        LEFT JOIN phone_info ON contacts.id = phone_info.contact_id
        LEFT JOIN email_info ON contacts.id = email_info.contact_id
        WHERE contacts.id = %s
    """, (id,))
    contact = cur.fetchone()  # fetch one record
    cur.close()
    return contact

def add_contact(mysql, name, phone, email, group_name):
    cur = mysql.connection.cursor()
    # Insert into contacts table first
    cur.execute("INSERT INTO contacts (name, group_name) VALUES (%s, %s)", (name, group_name))
    contact_id = cur.lastrowid
    
    # Insert into phone_info and email_info with the new contact_id
    cur.execute("INSERT INTO phone_info (contact_id, phone) VALUES (%s, %s)", (contact_id, phone))
    cur.execute("INSERT INTO email_info (contact_id, email) VALUES (%s, %s)", (contact_id, email))
    mysql.connection.commit()
    cur.close()

def edit_contact(mysql, id, name, phone, email, group_name):
    cur = mysql.connection.cursor()
    # Update contacts table
    cur.execute("UPDATE contacts SET name=%s, group_name=%s WHERE id=%s", (name, group_name, id))
    
    # Update phone_info and email_info tables
    cur.execute("UPDATE phone_info SET phone=%s WHERE contact_id=%s", (phone, id))
    cur.execute("UPDATE email_info SET email=%s WHERE contact_id=%s", (email, id))
    mysql.connection.commit()
    cur.close()

def delete_contact(mysql, id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()













from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.getcwd(), 'contacts.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            email TEXT,
                            address TEXT)''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        if name and phone:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                               (name, phone, email, address))
                conn.commit()
            return redirect(url_for('index'))
    return render_template('add_contact.html')

@app.route('/delete/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=True)
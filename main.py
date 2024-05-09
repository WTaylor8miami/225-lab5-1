from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS Information (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Address TEXT NOT NULL,
                Date TEXT NOT NULL,
                Email Text Not Null,
                Favorite_Food Text Not Null,
                Favorite_Drink Text Not Null
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            Information_id = request.form.get('Information_id')
            db = get_db()
            db.execute('DELETE FROM Information WHERE id = ?', (Information_id,))
            db.commit()
            message = 'Information deleted successfully.'
        else:
            Name = request.form.get('Name')
            Address = request.form.get('Address')
            Date = request.form.get('Date')
            Email = request.form.get('Email')
            Favorite_Food = request.form.get('Favorite_Food')
            Favorite_Drink = request.form.get('Favorite_Drink')
            if Name and Address and Date and Email and Favorite_Food and Favorite_Drink:
                db = get_db()
                db.execute('INSERT INTO Information (Name, Address, Date, Email, Favorite_Food, Favorite_Drink) VALUES (?, ?, ?, ?, ?, ?)', (Name, Address, Date, Email, Favorite_Food, Favorite_Drink))
                db.commit()
                message = 'Information added successfully.'
            else:
                message = 'Missing information.'

    # Always display the Information table
    db = get_db()
    Information = db.execute('SELECT * FROM Information').fetchall()

    # Display the HTML form along with the Information table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Food Information</title>
        </head>
        <body>
            <h2>Add Information</h2>
            <form method="POST" action="/">
                <label for="Name">Name:</label><br>
                <input type="text" id="Name" name="Name" required><br>
                <label for="Address">Address:</label><br>
                <input type="text" id="Address" name="Address" required><br>
                <label for="Date">Date:</label><br>
                <input type="text" id="Date" name="Date" required><br><br>
                <label for="Email">Email:</label><br>
                <input type="text" id="Email" name="Email" required><br><br>
                <label for="Favorite_Food">Favorite_Food:</label><br>
                <input type="text" id="Favorite_Food" name="Favorite_Food" required><br><br>
                <label for="Favorite_Drink">Favorite_Drink:</label><br>
                <input type="text" id="Favorite_Drink" name="Favorite_Drink" required><br><br>
                
                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if Information %}
                <table border="1">
                    <tr>
                        <th>Name</th>
                        <th>Address</th>
                        <th>Date</th>
                        <th>Email</th>
                        <th>Favorite_Food</th>
                        <th>Favorite_Drink</th>
                        <th>Delete</th>
                    </tr>
                    {% for Information in Information %}
                        <tr>
                            <td>{{ Information['Name'] }}</td>
                            <td>{{ Information['Address'] }}</td>
                            <td>{{ Information['Date'] }}</td>
                            <td>{{ Information['Email'] }}</td>
                            <td>{{ Information['Favorite_Food'] }}</td>
                            <td>{{ Information['Favorite_Drink'] }}</td>
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="Information_id" value="{{ Information['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No Information found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, Information=Information)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)

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
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ProductName TEXT NOT NULL,
                Reviewer TEXT NOT NULL,
                Date TEXT NOT NULL,
                ProductReview Text Not Null
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('reviews_id')
            db = get_db()
            db.execute('DELETE FROM reviews WHERE id = ?', (reviews_id,))
            db.commit()
            message = 'Contact deleted successfully.'
        else:
            ProductName = request.form.get('ProductName')
            Reviewer = request.form.get('Reviewer')
            Date = request.form.get('Date')
            ProductReview = request.form.get('ProductReview')
            if ProductName and Reviewer and date and ProductReview:
                db = get_db()
                db.execute('INSERT INTO reviews (ProductName, Reviewer, Date, ProductReview) VALUES (?, ?, ?, ?)', (ProductName, Reviewer, Date, ProductReview))
                db.commit()
                message = 'Review added successfully.'
            else:
                message = 'Missing information.'

    # Always display the contacts table
    db = get_db()
    contacts = db.execute('SELECT * FROM reviews').fetchall()

    # Display the HTML form along with the contacts table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reviews</title>
        </head>
        <body>
            <h2>Add Review</h2>
            <form method="POST" action="/">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="phone">Phone Number:</label><br>
                <input type="text" id="phone" name="phone" required><br><br>
                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if contacts %}
                <table border="1">
                    <tr>
                        <th>Name</th>
                        <th>Phone Number</th>
                        <th>Delete</th>
                    </tr>
                    {% for contact in contacts %}
                        <tr>
                            <td>{{ contact['name'] }}</td>
                            <td>{{ contact['phone'] }}</td>
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="reviews_id" value="{{ reviews['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No reviews found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, reviews=reviews)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)

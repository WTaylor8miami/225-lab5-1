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
            reviews_id = request.form.get('reviews_id')
            db = get_db()
            db.execute('DELETE FROM reviews WHERE id = ?', (reviews_id,))
            db.commit()
            message = 'Reviews deleted successfully.'
        else:
            ProductName = request.form.get('ProductName')
            Reviewer = request.form.get('Reviewer')
            Date = request.form.get('Date')
            ProductReview = request.form.get('ProductReview')
            if ProductName and Reviewer and Date and ProductReview:
                db = get_db()
                db.execute('INSERT INTO reviews (ProductName, Reviewer, Date, ProductReview) VALUES (?, ?, ?, ?)', (ProductName, Reviewer, Date, ProductReview))
                db.commit()
                message = 'Review added successfully.'
            else:
                message = 'Missing information.'

    # Always display the reviewss table
    db = get_db()
    reviews = db.execute('SELECT * FROM reviews').fetchall()

    # Display the HTML form along with the reviewss table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reviews</title>
        </head>
        <body>
            <h2>Add Review</h2>
            <form method="POST" action="/">
                <label for="Reviewer">Reviewer:</label><br>
                <input type="text" id="Reviewer" name="Reviewer" required><br>
                <label for="Date">Date:</label><br>
                <input type="text" id="Date" name="Date" required><br><br>
                <label for="ProductName">Product Name:</label><br>
                <input type="text" id="ProductName" name="ProductName" required><br><br>
                <label for="ProductReview">Product Review:</label><br>
                <input type="text" id="ProductReview" name="ProductReview" required><br><br>
                
                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if reviews %}
                <table border="1">
                    <tr>
                        <th>Reviewer</th>
                        <th>Date</th>
                        <th>Product Name</th>
                        <th>Prodcut Review</th>
                        <th>Delete</th>
                    </tr>
                    {% for reviews in reviews %}
                        <tr>
                            <td>{{ reviews['Reviewer'] }}</td>
                            <td>{{ reviews['Date'] }}</td>
                            <td>{{ reviews['ProductName'] }}</td>
                            <td>{{ reviews['ProductReview'] }}</td>
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

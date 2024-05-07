import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(reviews):
    """Generate test data for the contacts table."""
    db = connect_db()
    for i in range(reviews):
        product_name = f'Test Name {i}'
        reviewer = f'Test Name {i}'
        date = f'0-0-0000{i}'
        product_review = f'Product is great!{i}'
        db.execute('INSERT INTO reviews (Date, ProductName, Reviewer, ProductReview) VALUES (?, ?, ?, ?)', (date, product_name, reviewer, product_review))
    db.commit()
    print(f'{reviews} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test contacts.

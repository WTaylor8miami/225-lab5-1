import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_reviews):
    """Generate test data for the reviews table."""
    db = connect_db()
    for i in range(num_reviews):
        ProductName = f'Test Name {i}'
        Reviewer = f'Test Name {i}'
        Date = f'Test Name{i}'
        ProductReview = f'Test Name!{i}'
        db.execute('INSERT INTO reviews (Date, ProductName, Reviewer, ProductReview) VALUES (?, ?, ?, ?)', (Date, ProductName, Reviewer, ProductReview))
    db.commit()
    print(f'{num_reviews} test reviews added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test reviews.

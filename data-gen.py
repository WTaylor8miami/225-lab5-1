import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_Information):
    """Generate test data for the Information table."""
    db = connect_db()
    for i in range(num_Information):
        Name = f'Test Name {i}'
        Address = f'Test Address {i}'
        Date = f'Test Name{i}'
        Email = f'Test Email!{i}'
        Favorite_Food = f'Test Food!{i}'
        Favorite_Drink = f'Test Drink!{i}'
        db.execute('INSERT INTO Information (Name, Address, Date, Email, Favorite_Food, Favorite_Drink) VALUES (?, ?, ?, ?, ?, ?)', (Name, Address, Date, Email, Favorite_Food, Favorite_Drink))
    db.commit()
    print(f'{num_Information} test Information added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test reviews.

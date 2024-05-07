import sqlite3

# Database file path, ensure this matches the path used in your Flask application
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_test_data():
    """Clear only the test reviews from the database."""
    db = connect_db()
    # Assuming all test reviews follow a specific naming pattern
    db.execute("DELETE FROM reviews WHERE name LIKE 'Test Name %'")
    db.commit()
    print('Test data has been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_test_data()

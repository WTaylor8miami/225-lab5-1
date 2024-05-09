import sqlite3

# Database file path, ensure this matches the path used in your Flask application
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_test_data():
    """Clear only the test Information from the database."""
    db = connect_db()
    # Assuming all test Information follow a specific naming pattern
    db.execute("DELETE FROM Information WHERE Name LIKE 'Test Name %'")
    db.commit()
    print('Test Information has been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_test_data()

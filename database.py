import sqlite3

# Function to create a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('library.db')
    return conn

# Function to create the necessary tables
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            year INTEGER,
            rating FLOAT,
            status TEXT DEFAULT 'Unread',
            image BLOB  -- Add image column to store book cover images
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book_bucket_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    conn.commit()
    conn.close()

# Ensure the table is created when the module is imported
create_table()

# Function to add a book to the library
def add_book(title, author, genre, year, rating, status, image=None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, genre, year, rating, status, image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, genre, year, rating, status, image))
    conn.commit()
    conn.close()

# Function to get all books from the library
def get_all_books():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return books

# Function to update the status of a book
def update_book_status(book_id, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books
        SET status = ?
        WHERE id = ?
    ''', (status, book_id))
    conn.commit()
    conn.close()

# Function to delete a book from the library
def delete_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

# Function to check if a book is already in the Book Bucket List
def is_book_in_bucket_list(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book_bucket_list WHERE book_id = ?', (book_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None  # Returns True if the book is already in the bucket list

# Function to add a book to the Book Bucket List
def add_to_book_bucket_list(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO book_bucket_list (book_id) VALUES (?)', (book_id,))
    conn.commit()
    conn.close()

# Function to get all books in the Book Bucket List
def get_book_bucket_list():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT books.* FROM books
        JOIN book_bucket_list ON books.id = book_bucket_list.book_id
    ''')
    books = cursor.fetchall()
    conn.close()
    return books
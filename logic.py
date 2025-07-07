# logic.py
from tkinter import messagebox
from db_connect import cursor, conn

def register_member(roll, name):
    if not roll or not name:
        messagebox.showwarning("Input Error", "All fields are required.")
        return
    try:
        cursor.execute("INSERT INTO members (roll_no, name) VALUES (%s, %s)", (roll, name))
        conn.commit()
        messagebox.showinfo("Success", "Member registered.")
    except:
        messagebox.showerror("Error", "Member already exists.")

def add_book(title, author, copies):
    try:
        copies = int(copies)
    except:
        messagebox.showerror("Error", "Copies must be a number.")
        return

    cursor.execute("SELECT book_id FROM books WHERE title = %s AND author = %s", (title, author))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE books SET num_copies = num_copies + %s WHERE book_id = %s", (copies, result[0]))
    else:
        cursor.execute("INSERT INTO books (title, author, num_copies) VALUES (%s, %s, %s)", (title, author, copies))
    conn.commit()
    messagebox.showinfo("Success", "Book added.")

def delete_book(book_id):
    cursor.execute("SELECT num_copies FROM books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    if result:
        if result[0] > 1:
            cursor.execute("UPDATE books SET num_copies = num_copies - 1 WHERE book_id = %s", (book_id,))
        else:
            cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book deleted/reduced.")
    else:
        messagebox.showerror("Error", "Book ID not found.")

def issue_book(roll, book_id):
    cursor.execute("SELECT * FROM members WHERE roll_no = %s", (roll,))
    if cursor.fetchone() is None:
        messagebox.showerror("Error", "Member not found.")
        return

    cursor.execute("SELECT num_copies FROM books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    if not book or book[0] < 1:
        messagebox.showerror("Error", "No copies available.")
        return

    cursor.execute("INSERT INTO issued_books (roll_no, book_id) VALUES (%s, %s)", (roll, book_id))
    cursor.execute("UPDATE books SET num_copies = num_copies - 1 WHERE book_id = %s", (book_id,))
    conn.commit()
    messagebox.showinfo("Success", "Book issued.")

def return_book(roll, book_id):
    cursor.execute("SELECT issue_id FROM issued_books WHERE roll_no = %s AND book_id = %s LIMIT 1", (roll, book_id))
    issue = cursor.fetchone()
    if not issue:
        messagebox.showerror("Error", "Book not issued to this member.")
        return

    cursor.execute("DELETE FROM issued_books WHERE issue_id = %s", (issue[0],))
    cursor.execute("UPDATE books SET num_copies = num_copies + 1 WHERE book_id = %s", (book_id,))
    conn.commit()
    messagebox.showinfo("Success", "Book returned.")

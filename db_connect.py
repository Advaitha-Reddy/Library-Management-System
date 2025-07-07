import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",      
    password="advaitha",  
    database="school_library"
)
cursor = conn.cursor()

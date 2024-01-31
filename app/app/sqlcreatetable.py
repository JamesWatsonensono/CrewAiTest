import sqlite3

conn = sqlite3.connect('customer.db')

c = conn.cursor()

c.execute("""CREATE TABLE customers  (
            first_name text,
            last_name text,
            email text,
            phone integer,
            notes text
            ) """)
conn.commit()

conn.close()


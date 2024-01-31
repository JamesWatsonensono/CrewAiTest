import sqlite3

conn = sqlite3.connect('customer.db')

c = conn.cursor()

c.execute("select * from customers")

print(c.fetchall())
        
conn.commit()

conn.close()


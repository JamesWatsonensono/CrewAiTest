import sqlite3

conn = sqlite3.connect('customer.db')

c = conn.cursor()

c.execute("""INSERT INTO customers VALUES ('John', 'Elder', '122@bear.com', 1234567890, 'Phoned to compain about late delivery'
            ) """)
conn.commit()

conn.close()


    
    
import sqlite3
    
    
def get_data():
        """execute database query"""
        conn = sqlite3.connect('customer.db')
        cursor = conn.cursor()
        
        query = 'select * from customers'
        cursor.execute(query)
        
        rows = cursor.fetchall()
        
        # Assuming the customers table columns are: first_name, last_name, email, phone, notes
        customers_list = [{"first_name": row[0], "last_name": row[1], "email": row[2], "phone": row[3], "notes": row[4]} for row in rows]
        
        conn.close()
        
        return customers_list
        


print(get_data())




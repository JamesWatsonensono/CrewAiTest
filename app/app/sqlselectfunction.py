import sqlite3


get_data_declaration = {
    "name": "get_data",
    "description": "get data from database",
    
}

def get_data():
    conn = sqlite3.connect('customer.db')
    cursor = conn.cursor()
    
    query = "select * from customers"
    cursor.execute(query)
    
    rows = cursor.fetchall()
    
    list = [{"first_name":[0],"last_name":[1],"email":[2],"phone":[3],"notes":[4]}]
    
    conn.close()
    
    return list
 
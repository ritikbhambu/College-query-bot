import mysql.connector

# Establish connection
conn = mysql.connector.connect(
    host="localhost",        
    user="root",             
    password="ritik@sql",   
    database="clg_db",
    auth_plugin='mysql_native_password'      
)

# Cursor for running queries
cursor = conn.cursor()

# Test query
cursor.execute("SELECT * FROM departments LIMIT 5")

# Print all table names
for data in cursor.fetchall():
    print(data)

# Close connection
cursor.close()
conn.close()

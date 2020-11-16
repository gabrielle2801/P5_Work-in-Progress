import psycopg2


# declare a new PostgreSQL connection object
conn = psycopg2.connect(
	database="test_python", user='postgres', password='', host='localhost', port='5432'
	)
cursor = conn.cursor()

print ( conn.get_dsn_parameters(),"\n")
create_table_query = '''CREATE TABLE mobile
          (ID INT PRIMARY KEY     NOT NULL,
          MODEL           TEXT    NOT NULL,
          PRICE         REAL); '''
    
cursor.execute(create_table_query)
conn.commit()
print("Table created successfully in PostgreSQL ")
#Closing the connection
conn.close()


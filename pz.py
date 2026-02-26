import mysql.connector

cnx = mysql.connector.connect(
    host="srv221-h-st.jino.ru",
    database = "j30084097_137",
    user="j30084097_137",
    password="Gruppa137")

# Get a cursor
cur = cnx.cursor()

# Execute a query
cur.execute("SELECT CURDATE()")

# Fetch one result
row = cur.fetchone()
print("Current date is: {0}".format(row[0]))

# Close connection
cnx.close()
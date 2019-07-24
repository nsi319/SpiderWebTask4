import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd=""
)

cur=mydb.cursor()

cur.execute("CREATE DATABASE movies")

cur.execute('''USE movies''')

cur.execute('''CREATE TABLE users(
                 username VARCHAR(200),
                 password VARCHAR(200),
                 type VARCHAR(30))''')

cur.execute('''CREATE TABLE liked(
                  username VARCHAR(200),
                  title VARCHAR(200),
                  path VARCHAR(200))''')

cur.execute('''CREATE TABLE watched(
                  username VARCHAR(200),
                  title VARCHAR(200),
                  path VARCHAR(200))''')

cur.execute('''CREATE TABLE watchlater(
                  username VARCHAR(200),
                  title VARCHAR(200),
                  path VARCHAR(200))''')

cur.execute('''CREATE TABLE favourites(
                  username VARCHAR(200),
                  title VARCHAR(200),
                  path VARCHAR(200))''')

cur.execute('''CREATE TABLE comments(
                  username VARCHAR(200),
                  comment VARCHAR(200),
                  title VARCHAR(200))''')
 



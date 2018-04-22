from flask import Flask
from flask_mysqldb import MySQL
from data import Articles

app = Flask(__name__)
app.debug = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
Articles = Articles()

#Loads the different routes
from routes import *
from forms import *


if __name__ =='__main__':
    app.secret_key='secret123'
    app.run()

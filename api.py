import flask
import datetime
import mysql.connector
from flask import jsonify

app = flask.Flask(__name__)

app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

class create_dict(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

@app.route('/announcedinfos', methods=['GET'])
def get2ginfos():
  cnx = mysql.connector.connect(user='root', password='Skydrive0404', host='127.0.0.1', database='db_phones',auth_plugin='mysql_native_password')
  cursor = cnx.cursor()

  query = ("SELECT announcedInfo, count(uniqueID) as count  FROM db_phones.announcedtable group by (announcedInfo)")
  cursor.execute(query)
  rows = cursor.fetchall()

  results=[]
  for row in rows:
    results.append({"y":row[1],"name":row[0]})

  resp=jsonify(results)
  resp.headers.add('Access-Control-Allow-Origin', '*')
  cursor.close()
  cnx.close()
  return resp

  

app.run()
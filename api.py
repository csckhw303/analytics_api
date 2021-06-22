from os import abort
import flask
import datetime
import mysql.connector
from flask import jsonify
from flask import request, make_response
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
def getannouncedinfos():
  cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='db_phones',auth_plugin='mysql_native_password')
  cursor = cnx.cursor()

  query = ("SELECT announcedInfo, count(uniqueID) as count  FROM db_phones.announcedTable group by (announcedInfo)")
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

@app.route('/2Gbandsinfos', methods=['GET'])
def get2GBandinfos():
  cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='db_phones',auth_plugin='mysql_native_password')
  cursor = cnx.cursor()

  query = ("SELECT 2Gband, count(uniqueID) as count  FROM db_phones.2GbandsTable group by (2Gband)")
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

@app.route('/SIMinfos', methods=['GET'])
def getSIMinfos():
  cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='db_phones',auth_plugin='mysql_native_password')
  cursor = cnx.cursor()

  query = ("SELECT SIM, count(uniqueID) as count  FROM db_phones.SIMTable group by (SIM)")
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

@app.route('/wlaninfos', methods=['GET'])
def getwlaninfos():
  cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='db_phones',auth_plugin='mysql_native_password')
  cursor = cnx.cursor()

  query = ("SELECT wlan, GROUP_CONCAT(uniqueID) FROM wlanTable GROUP BY wlan")
  cursor.execute(query)
  rows = cursor.fetchall()

  results=[]

  for row in rows:
    results.append({"ids":row[1],"wlan":row[0]})

  resp=jsonify(results)
  resp.headers.add('Access-Control-Allow-Origin', '*')
  cursor.close()
  cnx.close()
  return resp

@app.route('/chipsetinfos', methods=['GET'])
def getchipsetinfos():
  cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='db_phones',auth_plugin='mysql_native_password')
  cursor = cnx.cursor()

  query = ("select chipset, GROUP_CONCAT(uniqueID) from db_phones.phones GROUP BY chipset ")
  cursor.execute(query)
  rows = cursor.fetchall()

  results=[]

  for row in rows:
    results.append({"ids":row[1],"chipset":row[0]})

  resp=jsonify(results)
  resp.headers.add('Access-Control-Allow-Origin', '*')
  cursor.close()
  cnx.close()
  return resp

@app.route('/search', methods=['OPTIONS','POST'])
def search():


  if request.method == 'OPTIONS': 
        return build_preflight_response()
  elif request.method == 'POST': 
        req = request.get_json()
        app.logger.info(req)
        cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='db_phones',auth_plugin='mysql_native_password')
        cursor = cnx.cursor()

        query = ("SELECT *  FROM db_phones.phones where uniqueid in (" + req['wlan'] + ")" + " or uniqueid in (" + req['chipset'] + ")")
        app.logger.info(query)
        cursor.execute(query)
        rows = cursor.fetchall()

        results=[]

        for row in rows:
           results.append({"name":row[2],"id":row[0], "image":row[4]})

        resp=jsonify(results)
        cursor.close()
        cnx.close()
        return build_actual_response(resp)

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



app.run()
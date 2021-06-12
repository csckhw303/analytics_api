import flask
import datetime
import mysql.connector

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/get2ginfos', methods=['GET'])
def get2ginfos():
  cnx = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='db_phones',auth_plugin='mysql_native_password')
  cursor = cnx.cursor()

  query = ("SELECT * FROM db_phones.2gbandstable")

  cursor.execute(query)

  for item in cursor:
    print("{}".format(item))

  cursor.close()
  cnx.close()

app.run()
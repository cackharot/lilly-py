from flask import Flask, request
import os
from bson import ObjectId
from bson import json_util as json
try:
    from flask_pymongo import PyMongo
except Exception as e:
    print("You should install flask-pymongo")
    print(e)

app = Flask(__name__)

app.config['MONGO_HOST'] = os.environ.get('MONGO_HOST')
app.config['MONGO_PORT'] = os.environ.get('MONGO_PORT','27107')
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME',app.name)
app.config['MONGO_USERNAME'] = os.environ.get('MONGO_USERNAME')
app.config['MONGO_PASSWORD'] = os.environ.get('MONGO_PASSWORD')
app.config['MONGO_CONNECT'] = False

mongo = PyMongo(app)

@app.route('/')
def home():
    message = [os.environ.get('MESSAGE', 'Hello World!')]
    message.append("<h2>ENVIRONMENT VARIABLES</h2>")
    message.append('<table>')
    for k,v in os.environ.items():
        message.append("<tr><td>%s</td><td>%s</td></tr>" % (k,v))
    message.append('</table>')
    return ''.join(message)

@app.route('/create',methods=['POST'])
def create():
    user = request.get_json()
    if user is None or ('name' not in user and len(user['name']) < 2):
        return json.dumps(dict(status='error',message='Invalid user')), 401
    user_id = mongo.db.users.save(user)
    return json.dumps(dict(status='success',href="/get?id=%s" % user_id)), 201

@app.route('/get')
def get_user():
    _id = request.args.get('id', None)
    if _id is None:
        return json.dumps(dict(status='error',message='id parameter required')), 401
    user = mongo.db.users.find_one_or_404({'_id':ObjectId(_id)})
    return json.dumps(dict(status='success',data=user))

if __name__ == '__main__':
    app.run(host='0.0.0.0')


# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from services.storage import sharedStorage

from modules.auth import *
from modules.protected import *
from modules.mysql import *
# from protected import *

# initialize main Flask object
if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some_secret_key'

    # register app blueprints
    app.register_blueprint(authRoute)
    app.register_blueprint(protectedRoute)

# make sure this is turned off
@app.after_request
def attachCORSHeader(response):
    response.headers.set('Access-Control-Allow-Headers', '*')
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response

# Publicly accessible routes
# ------------------------------
@app.route('/')
def home():
    output = []
    for user in sharedStorage.asList():
        output.append(str(user))
    return jsonify({
        'count': sharedStorage.totalCount(),
        'storage': output
    })

@app.route('/db')
def db():
    x = db.execute("SELECT VERSION() as version,NOW() as time")
    res = {}
    res["version"] = x[0][0]
    res["time"] = x[0][1]
    return jsonify(res)

# ---------------------------------
# Server start procedure
db = None
if __name__ == '__main__':
    db = Database(HOST, USER, PASS, DATA)
    if db == None:
        exit("Failed to connect to the database.")
    app.run(debug=True)

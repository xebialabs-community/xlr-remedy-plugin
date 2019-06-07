#!flask/bin/python
#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from flask import Flask
from flask import request
from flask import make_response
from functools import wraps
import os, io, json

app = Flask(__name__)

def getFile( fileName, status="200" ):
     filePath = "/remedy-stub/responses/%s" % fileName
     if not os.path.isfile(filePath):
        raise AuthError({"code": "response_file_not_found", "description": "Unable to load response file"}, 500)

     f = io.open(filePath, "r", encoding="utf-8")

     resp = make_response( (f.read(), status) )
     resp.headers['Content-Type'] = 'application/json; charset=utf-8'

     return resp

def requires_auth(f):
    """
    Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        if token != "DUMMY_TOKEN":
          raise AuthError({"code": "invalid_header", "description": "Unable to find appropriate key"}, 400)
        return f(*args, **kwargs)

    return decorated

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/arsys/v1/entry/<formName>/<entryId>', methods=['GET'])
@requires_auth
def getEntry(formName, entryId):
    return getFile("ticket_000000000000103.json")

@app.route('/api/arsys/v1/entry/<formName>?q=%27Infrastructure%20Change%20ID%27%3d%<changeId>%22', methods=['GET'])
@requires_auth
def checkStatus(formName, changeId):
    return getFile("ticket_CRQ000000152848.json")

@app.route('/api/arsys/v1/entry/<formName>', methods=['GET'])
@requires_auth
def getEntries(formName):
    return getFile("tickets.json")

@app.route('/api/arsys/v1/entry/<formName>', methods=['POST'])
@requires_auth
def createEntry(formName):
    fields = request.get_json()

    app.logger.info("createEntry = %s" % json.dumps(fields))

    resp = make_response(("", 201))
    resp.headers['Location'] = '/api/arsys/v1/entry/000000000000103'
    return resp

@app.route('/api/arsys/v1/entry/<formName>/<entryId>', methods=['PUT'])
@requires_auth
def updateEntry(formName, entryId):
    fields = request.get_json()

    app.logger.info("updateEntry = %s" % json.dumps(fields))

    resp = getFile("ticket_000000000000103.json", 204)
    resp.headers['Location'] = '/api/arsys/v1/entry/000000000000103'
    return resp

@app.route('/api/jwt/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    app.logger.info("URI = /api/jwt/login")
    app.logger.info("content: user=%s" % username)
    app.logger.info("content: password=%s" % password)

    if username == "xlr@xebialabs.com" and password == "admin":
        return "DUMMY_TOKEN"
    else:
        raise AuthError({"code": "credentials_invalid",
                        "description": "Credentials are invalid"}, 403)

def get_token_auth_header():
    """
    Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description": "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0] != "AR-JWT":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with AR-JWT"}, 401)
    token = parts[1]
    return token

if __name__ == '__main__':
    app.run(debug=True)

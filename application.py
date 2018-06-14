from sanic import Sanic
from sanic.response import json
from routes.auth import test
from mongoengine import *

app = Sanic()
connect('scrypt_db')

app.add_route(test, '/test/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
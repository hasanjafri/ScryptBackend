from sanic import Sanic
from sanic.response import json
from routes.auth import test, user_register
from mongoengine import connect

app = Sanic()
connect('scrypt_db')

app.add_route(test, '/test/')
app.add_route(user_register, '/user/register/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
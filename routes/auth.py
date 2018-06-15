from sanic.response import json
from mongoengine import *
from models.scrypt_user import scrypt_user
from clients.scrypt_user_mongodb_client import scrypt_user_mongodb_client

scrypt_user_client = scrypt_user_mongodb_client()

async def test(request):
    return(json({'hello': 'world'}))

async def user_register(request):
    jsonData = request.json

    if 'user_name' not in jsonData:
        return json({'error': 'Please enter your name'}, 400)
    else:
        user_name = jsonData['user_name']

    if 'user_email' not in jsonData:
        return json({'error': 'Please specify your email to login to Scrypt'}, 400)
    else:
        user_email = jsonData['user_email']

    if 'password' not in jsonData:
        return json({'error': 'Please enter a safe password to login to your Scrypt account'}, 400)
    else:
        password = jsonData['password']

    if 'picture' not in jsonData:
        return json({'error': 'Please choose an avatar for your Scrypt profile'}, 400)
    else:
        picture = jsonData['picture']

    return scrypt_user_client.user_register(user_name, user_email, password, picture)

async def user_login(request):
    jsonData = request.json

    if 'user_email' not in jsonData:
        return json({'error': 'Please enter the email associated with your Scrypt account'}, 400)
    else:
        user_email = jsonData['user_email']
    
    if 'password' not in jsonData:
        return json({'error': 'Please enter your password to login to Scrypt'}, 400)
    else:
        password = jsonData['password']

    return scrypt_user_client.user_login(user_email, password)

async def user_logout(request):
    jsonData = request.json

    if 'api_token' not in jsonData:
        return json({'error': 'Could not authenticate'}, 400)
    else:
        api_token = jsonData['api_token']

    return scrypt_user_client.user_logout(api_token)
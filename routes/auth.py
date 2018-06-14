from sanic.response import json
from mongoengine import *
from models.scrypt_user import scrypt_user

async def test(request):
    return(json({'hello': 'world'}))

async def user_register(request, user_info):
    pass
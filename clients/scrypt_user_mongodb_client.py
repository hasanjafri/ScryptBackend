from models.scrypt_user import scrypt_user
from mongoengine import *
from sanic.response import json
import secrets
from simplecrypt import encrypt, decrypt
from config import secret
from clients.scrypt_image_client import scrypt_image_client

class scrypt_user_mongodb_client(object):
    async def __init__(self):
        self.image_client = scrypt_image_client()

    async def check_user_exists(self, email):
        try:
            user = scrypt_user.objects(user_email=email)
        except Exception as e:
            return("Error \n %s" % (e))

        if len(user) > 0:
            return True
        else:
            return False

    async def generate_scrypt_token(self):
        api_token = secrets.token_urlsafe(32)
        if self.check_api_token_exists(api_token) == False:
            return api_token
        else:
            self.generate_scrypt_token()

    async def check_api_token_exists(self, api_token):
        check_api_token = scrypt_user.objects(scrypt_token=api_token)
        if len(check_api_token) > 0:
            self.generate_scrypt_token()
        else:
            return False

    async def encrypt_password(self, password):
        encrypted_pw = encrypt(secret, password.encode('utf-8'))
        return encrypted_pw

    async def verify_password(self, password, encrypted_pw):
        decrypted_pw = decrypt(secret, encrypted_pw)
        password_string = decrypted_pw.decode('utf-8')
        if password_string == password:
            return True
        else:
            return False

    async def check_valid_api_token(self, api_token):
        valid_token = scrypt_user.objects(scrypt_token=api_token)
        if len(valid_token) > 0:
            return True
        else:
            return False

    async def user_login(self, user_email, password):
        if not user_email:
            return json({'error': 'Please specify your email to login to Scrypt'})
        if not password:
            return json({'error': 'Please type your password'})

        if self.check_user_exists(user_email) == True:
            try:
                get_password = scrypt_user.objects(user_email=user_email)
                encrypted_pw = get_password[0].password
            except Exception as e:
                return("Error \n %s" % (e))

            if self.verify_password(password, encrypted_pw) == True:
                api_token = self.generate_scrypt_token()
                try:
                    scrypt_user.objects(user_email=user_email).update_one(upsert=False, set__scrypt_token=api_token)
                except Exception as e:
                    return("Error \n %s" % (e))
                
                user_name = get_password[0].user_name
                profile_pic = get_password[0].picture_path
                return json({'user_name': user_name, 'profile_pic': profile_pic, 'api_token': api_token})
            else:
                return json({'error': 'Incorrect password'})
        else:
            return json({'error': 'No user exists with this email'})

    async def user_logout(self, api_token):
        if not api_token:
            return json({'error': 'Could not authenticate'})

        if self.check_valid_api_token(api_token) == True:
            try:
                scrypt_user.objects(scrypt_token=api_token).update_one(upsert=False, set__scrypt_token='NULL')
            except Exception as e:
                return json({'error': "Error %s" % (e)})
            return json({'status': 'Logged out successfully'})
        else:
            return json({'error': 'Could not authenticate'})

    async def user_register(self, user_name, user_email, password, picture):
        if not user_name:
            return json({'error': 'Please enter your name'})
        if not user_email:
            return json({'error': 'Please specify your email to login to Scrypt'})
        if not password:
            return json({'error': 'Please enter a safe password to login to your Scrypt account'})
        if not picture:
            return json({'error': 'Please choose an avatar for your Scrypt profile'})

        if self.check_user_exists(user_email) == True:
            return json({'error': 'User already exists with this email address'})
        else:
            encrypted_pw = self.encrypt_password(password)
            api_token = self.generate_scrypt_token()
            image_url = self.image_client.save_image(picture)
            if 'error' in image_url:
                return json(image_url)
            else:
                try:
                    scrypt_user.objects(user_email=user_email).update_one(upsert=True, set__user_name=user_name, 
                     set__user_email=user_email, set__password=encrypted_pw, set__picture_path=image_url, set__scrypt_token=api_token)
                except Exception as e:
                    return json({'error': "Error %s" % (e)})
                return self.user_login(user_email, password)

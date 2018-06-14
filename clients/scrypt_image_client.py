import secrets
import base64
import os
from pathlib import Path
from sanic.response import json

class scrypt_image_client(object):
    async def generate_unique_name(self):
        image_name = secrets.token_urlsafe(32)
        if self.check_name_exists(image_name) == False:
            return(''+image_name+'.png')
        else:
            self.generate_unique_name()

    async def check_name_exists(self, name):
        image_path = Path("./images/"+name)
        if image_path.is_file():
            return True
        else:
            return False

    async def update_image_path(self, current_path, imagedata):
        if not current_path:
            return {'error': 'No current image path provided to update'}
        if not imagedata:
            return {'error': 'No new image provided to replace old image'}

        if self.check_name_exists(current_path) == True:
            if self.delete_image(current_path) == True:
                return self.save_image(imagedata)
            else:
                return {'error': 'Deletion of old image failed'}
        else:
            return {'error': 'Current image path provided does not exist'}

    async def save_image(self, imagedata):
        if not imagedata:
            return {'error': 'No image provided'}
        
        b64string = imagedata.encode()

        file_name = self.generate_unique_name()
        with open('./images/'+file_name, 'wb') as f:
            f.write(base64.decodebytes(b64string))

        if self.check_name_exists(file_name) == True:
            return file_name

    async def delete_image(self, current_path):
        if self.check_name_exists(current_path) == True:
            try:
                os.remove('./images/'+current_path)
            except Exception as e:
                return {'error': "Error %s" % (e)}

            if self.check_name_exists(current_path) == False:
                return True
            else:
                self.delete_image(current_path)

    
    
            
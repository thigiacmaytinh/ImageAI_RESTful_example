from django.conf import settings as djangoSettings
import os
import random
import string
from api.apps import *
import base64
import re

def SaveBase64ToImg(folder_name, file_name, images):
    if(images == None or images == "" ):
        return ""

    upload_folder_abs = os.path.join(djangoSettings.MEDIA_ROOT, folder_name)
    if not os.path.exists(upload_folder_abs):
        os.makedirs(upload_folder_abs)

    has_multiple_images = True if images.count("|") > 1 else False
    images = images.replace(" ", "+")
    if has_multiple_images:
        images = images.split("|")
    uploaded_file_urls = ""

    if has_multiple_images:
        for img in images:
            if(len(img) == 0):
                continue
            random_name = GenerateRandomName(file_name)
            save_file = os.path.join(upload_folder_abs, random_name)
            uploadfile = base64.b64decode(img)
            with open(save_file, 'wb') as f:
                f.write(uploadfile)
            uploaded_file_url = djangoSettings.MEDIA_URL + folder_name + "/" + random_name
            uploaded_file_urls = uploaded_file_urls  +  ";" + uploaded_file_url
        uploaded_file_urls = uploaded_file_urls[1:]
    else:
        random_name = GenerateRandomName(file_name)
        save_file = os.path.join(upload_folder_abs, random_name)
        uploadfile = base64.b64decode(images)
        with open(save_file, 'wb') as f:
            f.write(uploadfile)
        uploaded_file_url = djangoSettings.MEDIA_URL + folder_name + "/" + random_name
        uploaded_file_urls = uploaded_file_url
    return uploaded_file_urls

def urlify(s):
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+", '-', s)
    return s

def GenerateRandomName(name):
    fileName, fileEx = os.path.splitext(name)
    fileName = urlify(fileName)
    return fileName + '.' +''.join(random.choices(string.ascii_lowercase + "_" + string.ascii_uppercase +  string.digits, k=10)) + fileEx
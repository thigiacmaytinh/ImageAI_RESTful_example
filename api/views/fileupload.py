from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.core.files.storage import FileSystemStorage
from django.conf import settings as djangoSettings
import os
import random
import string
from api.apps import *
import base64
from api.saveBase64Image import *
from PIL import Image
import datetime
from imageai.Detection import ObjectDetection
import tensorflow as tf

####################################################################################################

execution_path = os.getcwd()



@api_view(["POST"])           
def UploadFile(request):
    try:

        if request.method != 'POST' or request.FILES['uploadfile'] == None:
            return Response(
                {'Error': "Thiếu tham số"},
                status=ERROR_CODE, content_type="application/json")

        #get image data
        uploadfile = request.FILES['uploadfile']            

        #set path
        upload_folder_abs = os.path.join(djangoSettings.MEDIA_ROOT)
        random_name = GenerateRandomName(uploadfile.name)
        saved_file_abs = os.path.join(upload_folder_abs, random_name)

        #save file
        fs = FileSystemStorage(upload_folder_abs)
        filename = fs.save(random_name , uploadfile)    
        

        #output path
        tempFilePath = upload_folder_abs + "\\temp.jpg"
        


        #load image to detect object
        strResult = ""
        #objects = detector.detectObjectsFromImage(input_image='D:\\img.jpg', output_image_path='D:\\output.jpg', minimum_percentage_probability=30)


        g_detector = ObjectDetection()
        g_detector.setModelTypeAsRetinaNet()
        g_detector.setModelPath( "resnet50_coco_best_v2.0.1.h5")
        g_detector.loadModel()
        objects = g_detector.detectObjectsFromImage(input_image=saved_file_abs, output_image_path=tempFilePath)

        for eachObject in objects:
            strResult += eachObject["name"] + " : " + str(eachObject["percentage_probability"]) + "\n"
            print(eachObject["name"] + " : " + str(eachObject["percentage_probability"]) )

        

        #convert output image to base64
        base64Str =""
        with open(tempFilePath, "rb") as image_file:
            base64Str = base64.b64encode(image_file.read())

        #result is json object
        result = {
            "num" : len(objects),
            "text" : strResult,
            "img": base64Str}


        #remove tempfile
        os.remove(saved_file_abs)
        os.remove(tempFilePath)


        return Response(
            result,
            status=SUCCESS_CODE, content_type="application/json")
    except Exception as e:
        return Response(
                {'Error': str(e)},
                status=ERROR_CODE, content_type="application/json")

####################################################################################################

@api_view(["POST"])           
def uploadbase64(request):
    try:
        folder_name = request.POST.get("folder_name")
        file_name = request.POST.get("file_name")
        images = request.POST.get("imgs")
        uploaded_file_urls = SaveBase64ToImg(folder_name, file_name, images)
        respond = {"url" : uploaded_file_urls}

        return Response(
                {respond},
                content_type="application/json",
                status=SUCCESS_CODE)
   
    except Exception as e:
        print(str(e))
        return Response(
                {'Error': str(e)},
                status=ERROR_CODE,
                content_type="application/json"
                )


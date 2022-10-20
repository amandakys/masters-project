from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
import os, uuid
import base64
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from deepar.utils import azure_has_blob, upload_file_to_azure
from restaurant_review.models import Profile
from .models import Image
from django.core.files.base import ContentFile
from datetime import date 
from azure.storage.blob import BlobServiceClient
from django.views.generic.base import TemplateView

# Create your views here.

def index(request):

    if request.method == 'POST':
        # this works

        #is AR image
        isAR = bool(request.META.get('HTTP_X_IS_AR'))
        img_data = request.body[22:]
        user = request.user.username

        user_path = "media/" + user
        local_path = user_path + '/experimentone'
        if not os.path.exists(user_path):
            os.mkdir(user_path)
            os.mkdir(local_path)
        elif not os.path.exists(local_path): 
            os.mkdir(local_path)

        # Create a file in the local data directory to upload and download
        today = date.today().strftime("%d-%m-%Y")
        # ar_file_name = today + ".png"
        # nar_file_name = today + "-unedited.png"
        ar_file_name = "edited.png"
        nar_file_name = "unedited.png"

        if isAR: 
            if not os.path.isfile(os.path.abspath(local_path + '/' + ar_file_name)):
                with open(os.path.abspath(local_path + '/' + ar_file_name), 'wb') as f: 
                    f.write(base64.decodebytes(img_data)) 
                    print("wrote to " + ar_file_name)
                    upload_file_to_azure(ar_file_name, user)

            else :
                print (ar_file_name + ' already exists')
        else: 
            if not os.path.isfile(os.path.abspath(local_path + '/' + nar_file_name)):
                with open(os.path.abspath(local_path + '/' + nar_file_name), 'wb') as f: 
                    f.write(base64.decodebytes(img_data)) 
                    print("wrote to " + nar_file_name)
                    upload_file_to_azure(nar_file_name, user)
            else :
                print (nar_file_name + ' already exists')
        
        #Clean up
        # os.remove(upload_file_path)
        # os.rmdir(local_path)

        return HttpResponse('post')

    return render(request, 'deepar.html')

def filters(request):
    return render(request, 'deepar_filters.html')

def select(request):
    if request.method == "GET":
        if request.user.is_authenticated: 
            profile = Profile.objects.get(user=request.user)
            return render(request, 'select.html', {'profile': profile})

    if request.method == "POST": 
        # result = request.body
        # print(result)
        result = bool(request.META.get('HTTP_X_RESULT'))
        profile = Profile.objects.get(user=request.user)
        profile.experiment_one_result = result 
        profile.experiment_one = True
        profile.save()
    # if azure_has_blob
    # if request.method == 'GET':
    #     # photo = response.content
    #     return render(request, 'select.html', {'photo', photo})

    return render(request, 'select.html')

def complete(request):
    return render(request, 'complete.html')
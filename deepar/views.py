from urllib.request import urlopen
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
import os, uuid
import base64
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from .models import Image
from django.core.files.base import ContentFile
from datetime import date 
from azure.storage.blob import BlobServiceClient

# Create your views here.
def index(request):
    if request.method == 'POST':
        # this works
        img_data = request.body[22:]
        user = request.user.username

        local_path = 'media/' + user 
        if not os.path.exists(local_path):
            os.mkdir(local_path)
        
        # Create a file in the local data directory to upload and download
        today = date.today().strftime("%d-%m-%Y")
        local_file_name = today + ".png"

        with open(os.path.abspath(local_path + '/' + local_file_name), 'wb') as f: 
            f.write(base64.decodebytes(img_data)) 

        connect_str = "DefaultEndpointsProtocol=https;AccountName=mastersproject;AccountKey=VgzJTcn2ZqBXV/hXIAiBdi43oFf+9pcaqx67hhbnwAYPia9N5BzpuksvdWVqmG5U9ASY0Fh/wzez+AStGrAjog==;EndpointSuffix=core.windows.net"
        
        #  connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)


        upload_file_path = os.path.join("./media/"+user, local_file_name)


        print("\nChecking blob does not already exist ...")
        #check blob does not already exist 
        blob_name = user+'/'+ local_file_name
        container_client = blob_service_client.get_container_client("media")
        hasBlob = False

        blob_list = container_client.list_blobs()

        for blob in blob_list: 
            if blob.name == blob_name :
                hasBlob = True
                print('File already exists')

        if not hasBlob:
            # Create a blob client using the local file name as the name for the blob
            blob_client = blob_service_client.get_blob_client(container='media', blob=blob_name)

            print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

            # Upload the created file
            with open(upload_file_path, "rb") as data:
                blob_client.upload_blob(data)

        

        # blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # upload_file_path = os.path.join('../media', 'test.png')

        # blob_client = blob_service_client.get_blob_client(container='media', blob='test.png')

            
        # # Upload the created file
        # with open(upload_file_path, "rb") as data:
        #     blob_client.upload_blob(data)

        return HttpResponse('post')

    return render(request, 'deepar.html')
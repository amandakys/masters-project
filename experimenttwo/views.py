import base64
from datetime import date
import json
import os
from django.shortcuts import redirect, render

from deepar.utils import delete_file, upload_file_to_azure
from restaurant_review.models import Profile

# Create your views here.

def camera(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        profile.experiment_two_day += 1
        profile.experiment_two_last_photo_date = date.today()
        profile.save()
    
    if request.method == 'POST':
        #increment day and last photo taken variables 


        isAR = bool(request.META.get('HTTP_X_IS_AR'))
        img_data = request.body[22:]
        user = request.user.username

        user_path = "media/" + user
        local_path = user_path + '/experimenttwo'
        if not os.path.exists(user_path):
            os.mkdir(user_path)
            os.mkdir(local_path)
        elif not os.path.exists(local_path): 
            os.mkdir(local_path)

        # Create a file in the local data directory to upload and download
        # today = date.today().strftime("%d-%m-%Y")
        today = 'day' + str(profile.experiment_two_day)
        ar_file_name = today + "-edited.png"
        nar_file_name = today + "-unedited.png"

        if isAR: 
            if not os.path.isfile(os.path.abspath(local_path + '/' + ar_file_name)):
                with open(os.path.abspath(local_path + '/' + ar_file_name), 'wb') as f: 
                    f.write(base64.decodebytes(img_data)) 
                    print("wrote to " + ar_file_name)
                    blob_name = user + '/experimenttwo/'+ ar_file_name
                    upload_file_to_azure(blob_name)

            else :
                print (ar_file_name + ' already exists')
        else: 
            if not os.path.isfile(os.path.abspath(local_path + '/' + nar_file_name)):
                with open(os.path.abspath(local_path + '/' + nar_file_name), 'wb') as f: 
                    f.write(base64.decodebytes(img_data)) 
                    print("wrote to " + nar_file_name)
                    blob_name = user + '/experimenttwo/'+ nar_file_name
                    upload_file_to_azure(blob_name)
            else :
                print (nar_file_name + ' already exists')
        

    return render(request, 'deepar.html', {'profile': profile})

def next(request):
    # if request.method == 'GET': 
    profile = Profile.objects.get(user=request.user)
    if profile.experiment_two_day == 6: 
        return redirect('select_three')

    # profile = Profile.objects.get(user=request.user)

    return render(request, 'next.html', {'profile': profile})

def select(request):
    if request.method == "POST":
        data = json.loads(request.body)
        profile = Profile.objects.get(user=request.user)


        print(data['edited'])
        print(data['selection'])
        print(data['numEditedSelected'])
        profile.experiment_two_selection = data['selection']
        profile.experiment_two_edited = data['edited']
        profile.experiment_two = True
        profile.experiment_two_num_edited_selected = data['numEditedSelected']
        profile.save()
    return render(request, 'select_three.html')

def finished(request):
    if request.method == 'POST':
        user = request.user.username
        for i in range(1,7):

            edited = user + '/experimenttwo/day' + str(i) + '-edited.png'
            unedited = user + '/experimenttwo/day' + str(i) + '-unedited.png'
            print('deleting edited')
            delete_file(edited)
            print('deleting unedited')
            delete_file(unedited)

    return render(request, 'finished.html')
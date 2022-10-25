# accounts/views.py
from tokenize import group
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


from restaurant_review.models import Profile



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    # def post(self, request):
    #     super(SignUpView, self).post(request)
        

    #     login_username = request.POST['username']
    #     print(login_username)
    #     # login_password = request.POST['password1']
    #     # created_user = authenticate(username=login_username, password=login_password)

    #     # login(request, created_user)
    #     return redirect('/')

    def form_valid(self, form):
        form.save()
        # super(SignUpView, self).form_valid(form)
        username = self.request.POST['username']
        print(username)


        password = self.request.POST['password1']
        #authenticate user then login
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
        numUsers = User.objects.count()
        print(numUsers)
        profile = Profile.objects.get(user=user)
        groupNumber = numUsers%6

  
        if groupNumber == 0: 
            print('group 0')
            profile.isARCamera = False
            profile.tellIsAR = False
            profile.showARImage = False
        elif groupNumber == 1:
            print('group 1')
            profile.isARCamera = False
            profile.tellIsAR = False
            profile.showARImage = True
        elif groupNumber == 2:
            print('group 2')
            profile.isARCamera = True
            profile.tellIsAR = False
            profile.showARImage = False
        elif groupNumber == 3:
            print('group 3')
            profile.isARCamera = True
            profile.tellIsAR = False
            profile.showARImage = True
        elif groupNumber == 4:
            print('group 4')
            profile.isARCamera = True
            profile.tellIsAR = True
            profile.showARImage = False
        else: 
            print('group 5')
            profile.isARCamera = True
            profile.tellIsAR = True
            profile.showARImage = True
            
        # if numUsers % 3 == 0 : 
        #     if numUsers % 6 == 0:
        #         # group 6
        #         print('group 6')
        #         profile.showARImage = False
        #     else:
        #         # group 3
        #         print('group 3')
        #         profile.isARCamera = True
        #         profile.tellIsAR = True
        #         profile.showARImage = True

        # elif numUsers % 2 == 0:
        #     if numUsers % 4 == 0:
        #          # group 4
        #         print('group 4')
        #         profile.showARImage = False
        #     else:
        #         # group 2
        #         print('group 2')
        #         profile.isARCamera = True
        #         profile.tellIsAR = False
        #         profile.showARImage = True
        # else :
        #     if numUsers % 5 == 0:
        #          # group 5
        #         print('group 5')
        #         profile.showARImage = False
        #     else: 
        #         # group 1
        #         print('group 1')
        #         profile.isARCamera = False
        #         profile.tellIsAR = False
        #         profile.showARImage = True
    
        profile.save()
        
        login(self.request, user)
        return redirect(self.success_url)
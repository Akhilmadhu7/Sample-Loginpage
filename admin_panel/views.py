from asyncio.sslproto import _create_transport_context
from collections import UserList
from email import message
from operator import index
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
import re

# Create your views here.


### ADMIN PANEL SIGNUP ###  

cache_control(no_cache = True, must_revalidate = True, no_store =True)

def adminsignin(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        adminuser = authenticate(username=username,password=password)

        if adminuser is not None and adminuser.is_superuser:
            request.session['username'] = username
            login(request,adminuser)
            return redirect(index)

        else:

            messages.error(request,'Invalid details')
            return redirect(adminsignin)

    return render(request,'admintemplates/signin.html')

### INDEX PAGE FUNCTION ###


cache_control(no_cache = True, must_revalidate = True, no_store =True)

def index(request):

    if 'username' in request.session:

        userdata = User.objects.all()
        return render(request,'admintemplates/index.html',{'userlist':userdata})

    return render(request,'admintemplates/signin.html')   


### ADMIN PANEL LOGOUT FUNCTION ###  


def adminsignout(request):

    if 'username' in request.session:
        request.session.flush()
        logout(request)

    return redirect(adminsignin)    

### CREATE NEW ACCOUNT FUNCTION ### 


def createacnt(request):

    if request.method == 'POST':
         username = request.POST.get('username')
         email = request.POST.get('email')
         password1 = request.POST.get('password1')
         password2 = request.POST.get('password2')

         ### USERNAME VERIFICATION ### 

         username_pattern = "^[A-Za-z\s]{3,}$"
         username_verify = re.match(username_pattern,username)

         if username_verify is None:
            messages.error(request,'Username must be characters only')
            return redirect(createacnt)

         if User.objects.filter(username = username):
            messages.error(request,'Username already exists')
            return redirect(createacnt)

        ### EMAIL VERIFICATION ###

         email_pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
         email_verify = re.match(email_pattern,email)

         if email_verify is None:
            messages.error(request,'Invalid email')        
            return redirect(createacnt)

         if User.objects.filter(email=email):
            messages.error(request,'Email already exists')
            return redirect(createacnt)

        ### PASSWORD VERIFICATION ###  

         password_pattern = "^[a-zA-Z0-9]{8}[0-9]*[A-Za-z]*$"      
         password_verify = re.match(password_pattern,password1)

         if password_verify is None:
            messages.error(request,'Password at least contain 8 characters')
            return redirect(createacnt)

         if password1 != password2:
            messages.error(request,'Incorrect password')
            return redirect(createacnt)

         else:

            newuser = User.objects.create_user(username=username,email=email,password=password1)
            newuser.save()
            messages.info(request,'Data has been added')

            userdata = User.objects.all()

            return render(request,'admintemplates/index.html',{'userlist':userdata})

    return render(request,'admintemplates/createacnt.html') 


### UPDATE FUNCTION ### 


def update(request,id):

    user = User.objects.get(id=id)
    if request.method == 'POST':

        newusername = request.POST.get('username')
        newemail = request.POST.get('email')
        
        user.username = newusername
        user.email = newemail
        user.save()
        messages.info(request,'Data succesfully uodated')
        return redirect(index)

    return render(request,'admintemplates/update.html',{'userdata':user})


### DELETE FUNCTION ### 


def delete(request,id):

    userdel = User.objects.get(id=id)
    userdel.delete()
    messages.info(request,'Data deleted succesfully')
    return redirect(index)

### SEARCH FUNCTION ###  


def search(request):

    if request.method == 'POST':
        searchvalue = request.POST.get('search')
        searchdata = User.objects.filter(username__icontains = searchvalue)

    context = {
            'searchresult':searchdata
        }
    return render(request,'admintemplates/search.html',context)











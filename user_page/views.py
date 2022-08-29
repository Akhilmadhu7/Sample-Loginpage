from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib import messages
import re

# Create your views here.

### USER LOGIN FUNCTION ###

@cache_control(no_cache = True, must_revalidate = True, no_store = True)

def user_login(request):

    if 'username' in request.session:
        return redirect(homepage)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            request.session['username'] = username

            login(request,user)

            return redirect(homepage)

        else:
            messages.error(request,'Invalid Details')  
            return redirect(user_login)  

    return render(request,'usertemplates/userlog.html') 

### USER HOME FUNCTION ###

@cache_control(no_cache = True, must_revalidate = True, no_store = True)

def homepage(request):

    if 'username' in request.session:
        return render(request,'usertemplates/userhome.html')

    return redirect(user_login)


 ### USER LOGOUT FUNCTION ###


def user_logout(request):  

    if 'username' in request.session:
        request.session.flush()
        logout(request)

    return redirect(user_login)   



### USER SIGIN UP FUNCTION ###


def user_signup(request):

    # user = User.objects.all()

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        ### USERNAME VERIFICATION ###

        username_pattern = "^[A-Za-z\s]{3,}$"
        username_verify = re.match(username_pattern,username)

        if username_verify is None:
            messages.error(request,'Name should contian only characters')
            return redirect(user_signup)

        if User.objects.filter(username=username):
            messages.error(request,'Username already exists') 
            return redirect(user_signup)

        ### EMAIL VERIFICATION ### 

        email_pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        email_verify = re.match(email_pattern,email)


        if email_verify is None:
            messages.error(request,'Invalid Email')
            return redirect(user_signup)

        if User.objects.filter(email=email):
            messages.error(request,'Email already exists')
            return redirect(user_signup)

        ### PASSWORD VERIFICATION ###    

        if password1 == "" or len(password1)<4:
            messages.error(request,'Password should contains atleast 5 letters')
            return redirect(user_signup)

        if password1 != password2:
            messages.error(request,'Password incorrect')
            return redirect(user_signup)


        else:

            user = User.objects.create_user(username=username,email=email,password=password1,)   
            user.save()
            return redirect(user_login)

    return render(request,'usertemplates/usersign.html')                


            


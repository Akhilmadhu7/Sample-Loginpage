from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_login,name='userlogin'),
    path('home_page',views.homepage,name='home_page'),
    path('userlogout',views.user_logout,name='userlogout'),
    path('usersignup',views.user_signup,name='usersignup')
]

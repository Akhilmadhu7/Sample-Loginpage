from django.urls import path
from . import views


urlpatterns = [
    path('adminsignin',views.adminsignin,name='adsignin'),
    path('index',views.index,name='index'),
    path('adminsignout',views.adminsignout,name='adsignout'),
    path('update/<int:id>/',views.update,name='adupdate'),
    path('createacnt',views.createacnt,name='adaccount'),
    path('index/search',views.search,name='usersearch'),
    path('delete/<int:id>/',views.delete,name='addelete')
]

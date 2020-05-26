from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'dashbord'

urlpatterns = [
    path('', views.dashbord, name='dashbord'),
    path('<str:bdname>/', views.allCompagne, name='allCompagne'),
    path('<str:bdname>/<int:mail_sending_id>', views.AnalysePerCompagne, name='AnalysePerCompagne'),
    path('users', views.allUsers, name='allUsers'),
    path('test', views.test, name='test'),
    #ajax function
    path('analyse/<int:mail_sending_id>/<str:type_device>/<str:mode_device>', views.updateGraph, name='updateGraph'),
]

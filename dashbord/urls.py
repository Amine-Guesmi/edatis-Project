from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'dashbord'

urlpatterns = [
    path('', views.dashbord, name='dashbord'),
    path('<str:bdname>/', views.allCompagne, name='allCompagne'),
    path('globalStat/<str:bdname>/', views.globalStat, name='globalStat'),
    path('<str:bdname>/<int:mail_sending_id>/contact', views.AnalysePerContact, name='AnalysePerContact'),
    path('<str:bdname>/<int:mail_sending_id>/compagne', views.AnalysePerCompagne, name='AnalysePerCompagne'),
    path('users', views.allUsers, name='allUsers'),
    path('test', views.test, name='test'),
    #ajax function
    path('analyse/contact', views.updateGraphContact, name='updateGraphContact'),
    path('analyse/compagne', views.updateGraphCompagne, name='updateGraphCompagne'),
    path('analyse/globalStat', views.updateGlobalStat, name='updateGlobalStat'),
]

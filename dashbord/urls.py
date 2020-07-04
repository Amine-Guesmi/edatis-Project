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
    path('recommandation', views.recommandationFuntion, name='recommandationFuntion'),
    path('<str:bdname>/allContact/<int:mail_sending_id>', views.allContact, name='allContact'),
    path('AnalyseIps/<dbname>', views.AnalyseIps, name='AnalyseIps'),
    path('test', views.test, name='test'),
    #ajax function
    path('analyse/contact', views.updateGraphContact, name='updateGraphContact'),
    path('analyse/compagne', views.updateGraphCompagne, name='updateGraphCompagne'),
    path('analyse/globalStat', views.updateGlobalStat, name='updateGlobalStat'),
    path('analyse/globalStats/dateStats', views.updateStatsPerDate, name='updateStatsPerDate'),
    path('recommandation/predict', views.recommandationAction, name='recommandationAction'),
    path('recommandation/compDetails/<int:id>', views.recommandationCompDetails, name='recommandationCompDetails'),
    path('recommandation/compDelete/<int:id>', views.recommandationDelete, name='recommandationDelete'),
    path('recommandation/compDeleteModal/<int:id>', views.recommandationDeleteModal, name='recommandationDeleteModal'),
    path('analyse/globalStats/sendMail', views.sendStatsMail, name='sendStatsMail'),
    path('allRecordsIps', views.getMailIpsStats, name='getMailIpsStats'),
]

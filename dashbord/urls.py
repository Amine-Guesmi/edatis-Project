from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'dashbord'

urlpatterns = [
    path('', views.dashbord, name='dashbord'),
    path('<str:bdname>/', views.allCompagne, name='allCompagne'),
    path('users', views.allUsers, name='allUsers'),
    path('users/activate/<str:username>', views.activateWaiter, name='activateWaiter'),
    path('test', views.test, name='test'),
]

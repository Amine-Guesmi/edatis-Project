from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'dashbord'

urlpatterns = [
    path('login', views.loginPage, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logoutPage, name='logout'),
    path('error403', views.error403, name='error403'),
]

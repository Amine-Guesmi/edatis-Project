from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'dashbord'

urlpatterns = [
    path('login', views.loginPage, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logoutPage, name='logout'),
    path('error403', views.error403, name='error403'),
    path('dashbord/users/create', views.user_create, name='user_create'),
    path('dashbord/users/<int:id>/update', views.user_update, name='user_update'),
    path('dashbord/users/<int:id>/delete', views.user_delete, name='user_delete'),
]

from django.conf.urls import url
from . import views

app_name = 'dashbord'

urlpatterns = [
    url(r'^$', views.dashbord, name='dashbord'),
]

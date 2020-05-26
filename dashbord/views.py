from django.shortcuts import render, redirect
import os, subprocess, json
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import User, Group
from django.contrib import messages
import logging
import subprocess
from django.http import JsonResponse
#import models
from .models import compte, compagne, Analyse
#Spark
import findspark
import pyspark
from pyspark.sql import *
from pyspark.sql.functions import col
#spark intance / Spark context / spark Session
findspark.init('/home/hduser/spark')
sc = pyspark.SparkContext(appName="Edatis Anlyses")
#spark = SparkSession(sc)
spark = SparkSession(sc).builder.config('spark.submit.deployMode','client').getOrCreate()
#logger instance
logger = logging.getLogger(__name__)



# function redirect to dashbord with all comptes of all users (Hub)
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin', 'DataAnalyst'])
def dashbord(request):
    df = spark.read.json("/dataLake/hub/compte").select("id", "name", "bddname", "active", "dateinscription")
    l= [list(row) for row in df.collect()]
    content = subprocess.Popen(["hdfs", "dfs", "-du", "-h", "-s", "/dataLake"], stdout=subprocess.PIPE)
    for line in content.stdout:
        aux = line.decode('utf-8')
    context = {
        'comptes' :  [compte(s[0], s[1], s[2], s[3], s[4]) for s in l] ,
        'numberActifClient' : df.where(df.active == True).count(),
        'sizeDataLake' : aux[:aux.find('G')],
        'pageName' : 'Dasbord'
    }
    return render(request, 'dashbord.html', context)

#function display Campagnes with id
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin', 'DataAnalyst'])
def allCompagne(request, bdname):
    df = spark.read.json("/dataLake/"+bdname+"/mail_sending").select("id", "name", "finish").distinct()
    l= [list(row) for row in df.collect()]
    context = {
        'compagnes' :[compagne(s[0], s[1], s[2]) for s in l] ,
        'bdname' : bdname,
        'pageName' : 'Compagnes Of '+bdname
    }
    return render(request, 'allcompagne.html', context)
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def allUsers(request):
    users = User.objects.all()
    context = {
        'users' : users
    }
    return render(request, 'allUsers.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def activateWaiter(request, username):
    user = User.objects.get(username=username)
    group_obj = Group.objects.get(name='DataAnalyst')
    user_group = User.groups.through.objects.get(user=user)
    user_group.group = group_obj
    user_group.save()
    messages.success(request, 'User updated successfully to DataAnalyst')
    return redirect('edatis_dashbord:allUsers')

def AnalysePerCompagne(request, bdname, mail_sending_id):

    Analyse_obj = Analyse()

    df_clic = spark.read.json("/dataLake/Tisseo/clic")
    df_link = spark.read.json("/dataLake/Tisseo/link")
    #open partie
    df = spark.read.json("/dataLake/"+bdname+"/open").select("tablet", "desktop", "mobile","mail_sending_id")
    Analyse_obj.tablet_open = df.where("tablet=1 AND mail_sending_id="+str(mail_sending_id)).count()
    Analyse_obj.Desktop_open= df.where("desktop=1 AND mail_sending_id="+str(mail_sending_id)).count()
    Analyse_obj.tel_open    = df.where("mobile=1 AND mail_sending_id="+str(mail_sending_id)).count()
    Analyse_obj.SumAllDevices = Analyse_obj.tablet_open + Analyse_obj.tel_open  + Analyse_obj.Desktop_open
    SumAllDevicesClic = df_clic.alias('c').join(df_link.alias('l'),col('l.id') == col('c.link_id')).where("mail_sending_id="+str(mail_sending_id)).count()
    context = {
        'Analyse_obj' : Analyse_obj,
        'pageName' : bdname+'Analyses',
        'SumAllDevicesClic' : SumAllDevicesClic,
        'mail_sending_id' :  mail_sending_id
    }
    return render(request, 'Analyse.html', context)

def updateGraph(request, mail_sending_id, type_device, mode_device):
    data['form_is_valid'] = True
    return JsonResponse(data)

def test(request):
    return render(request, 'error.html')

from django.shortcuts import render, redirect
import os, subprocess, json
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import User, Group
from django.contrib import messages
import logging
import subprocess
#import models
from .models import compte, compagne, Analyse
#Spark
import findspark
import pyspark
from pyspark.sql import *
#spark intance / Spark context / spark Session
findspark.init('/home/hduser/spark')
sc = pyspark.SparkContext(appName="myAppName")
spark = SparkSession(sc)
#logger instance
logger = logging.getLogger(__name__)

# function redirect to dashbord with all comptes of all users (Hub)
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin', 'DataAnalyst'])
def dashbord(request):
    df = spark.read.json("/dataLake/hub/compte")
    comptesJson = df.toJSON().map(lambda j: json.loads(j)).collect()
    comptes = []
    for jsonTranform in comptesJson:
        comptes.append(compte(jsonTranform['id'],  jsonTranform['name'], jsonTranform['bddname'], jsonTranform['active'], jsonTranform['dateinscription']))
    content = subprocess.Popen(["hdfs", "dfs", "-du", "-h", "-s", "/dataLake"], stdout=subprocess.PIPE)
    for line in content.stdout:
        aux = line.decode('utf-8')
    context = {
        'comptes' :  comptes,
        'numberActifClient' : df.where(df.active == True).count(),
        'sizeDataLake' : aux[:aux.find('G')]
    }
    return render(request, 'dashbord.html', context)

#function display Campagnes with id
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin', 'DataAnalyst'])
def allCompagne(request, bdname):
    try:
        compagnesJson  = spark.read.json("/dataLake/"+bdname+"/mail_sending").select("id", "name", "finish").distinct().toJSON().map(lambda j: json.loads(j)).collect()
    except:
        return render(request, 'error.html')
    compagnes = []
    for comp in compagnesJson:
        compagnes.append(compagne(comp['id'], comp['name'], comp['finish']))
    context = {
        'compagnes' : compagnes,
        'bdname' : bdname
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
    #open partie
    df = spark.read.json("/dataLake/"+bdname+"/open")
    Analyse_obj.tablet_open = df.select("tablet","mail_sending_id").where("tablet=1 AND mail_sending_id="+str(mail_sending_id)).count()
    Analyse_obj.tel_open    = df.select("mobile", "mail_sending_id").where("mobile=1 AND mail_sending_id="+str(mail_sending_id)).count()
    Analyse_obj.Desktop_open= df.select("desktop", "mail_sending_id").where("desktop=1 AND mail_sending_id="+str(mail_sending_id)).count()
    context = {
        'Analyse_obj' : Analyse_obj
    }
    return render(request, 'Analyse.html', context)

def test(request):
    return render(request, 'error.html')

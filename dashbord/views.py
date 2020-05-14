from django.shortcuts import render, redirect
import os, subprocess, json
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import User, Group
from django.contrib import messages
import logging
#import models
from .models import compte, compagne
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
    comptesJson = spark.read.json("/dataLake/hub/compte").toJSON().map(lambda j: json.loads(j)).collect()
    comptes = []
    for jsonTranform in comptesJson:
        comptes.append(compte(jsonTranform['id'],  jsonTranform['name'], jsonTranform['bddname'], jsonTranform['active'], jsonTranform['dateinscription']))
    context = {
        'comptes' :  comptes
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
        'compagnes' : compagnes
    }
    return render(request, 'allcompagne.html', context)

def allUsers(request):
    users = User.objects.all()
    print(users)
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

def test(request):
    return render(request, 'error.html')

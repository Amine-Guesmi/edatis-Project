from django.shortcuts import render, redirect
import os, subprocess, json
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import User, Group
from django.contrib import messages
import logging
import datetime
import subprocess
from django.http import HttpResponse, Http404
import time
import calendar
#machine leaning module
import pickle
#open Predict
model_open_desktop = pickle.load(open('/home/hduser/machine-Leaning/open_predict_devices/ContactClasification(open)(desktop).pkl', 'rb'))
model_open_mobile = pickle.load(open('/home/hduser/machine-Leaning/open_predict_devices/ContactClasification(open)(mobile).pkl', 'rb'))
model_open_tablet = pickle.load(open('/home/hduser/machine-Leaning/open_predict_devices/ContactClasification(open)(tablet).pkl', 'rb'))

#clic Predic
model_clic_desktop = pickle.load(open('/home/hduser/machine-Leaning/clic_predict_devices/ContactClasification(clic)(desktop)Tisso.pkl', 'rb'))
model_clic_mobile = pickle.load(open('/home/hduser/machine-Leaning/clic_predict_devices/ContactClasification(clic)(mobile)Tisso.pkl', 'rb'))
model_clic_tablet = pickle.load(open('/home/hduser/machine-Leaning/clic_predict_devices/ContactClasification(clic)(tablet)Tisso.pkl', 'rb'))
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
        'compagnes' :[compagne(s[0], s[1], s[2], 1) for s in l] ,
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

def AnalysePerContact(request, bdname, mail_sending_id):
    Analyse_obj = Analyse(0 ,0 ,0 ,0 ,0 , 0)
    '''
    for content in  spark.read.json("/dataLake/"+bdname+"/stat_hour").select("nbmailsend", "mail_sending_id","clicsdesktop", "clicstablet", "clicsmobile", "opensdesktop", "opensmobile", "openstablet").where("mail_sending_id = "+str(mail_sending_id)).collect():
        Analyse_obj.nbMailSending += content['nbmailsend']
        Analyse_obj.tablet_open += content['openstablet']
        Analyse_obj.tel_open += content['opensmobile']
        Analyse_obj.Desktop_open += content['opensdesktop']
        Analyse_obj.SumAllDevicesClic += (content['clicsdesktop']+content['clicstablet']+content['clicsmobile'])
    '''
    for content in  spark.read.json("/dataLake/"+bdname+"/open").select('mail_sending_id', "desktop", "tablet", "mobile").where("mail_sending_id = "+str(mail_sending_id)).collect():
        if content["desktop"] :
            Analyse_obj.Desktop_open += 1
        elif content["tablet"]:
            Analyse_obj.tablet_open += 1
        else:
            Analyse_obj.tel_open += 1
    Analyse_obj.SumAllDevicesOpen = (Analyse_obj.tablet_open + Analyse_obj.tel_open + Analyse_obj.Desktop_open )
    Analyse_obj.SumAllDevicesClic += 300

    context = {
        'Analyse_obj' : Analyse_obj,
        'pageName' : bdname+' Analyses',
        'mail_sending_id' :  mail_sending_id,
        'bdname' : bdname
    }
    return render(request, 'AnalyseContact.html', context)

def AnalysePerCompagne(request, bdname, mail_sending_id):

    statHour = spark.read.json("/dataLake/"+bdname+"/stat_hour")
    chart_open_clic, chart_sending_abotie, chart_devices_clic, chart_devices_open  = [0, 0], [0, 0], [0, 0, 0],[0, 0, 0]
    for content in  statHour.where("mail_sending_id ="+str(mail_sending_id)).collect():
        #chart_open clic
        chart_open_clic[0] += content["clics"]
        chart_open_clic[1] += content['opens']
        #chart sending abotie
        chart_sending_abotie[0] += content['nbmailsend']
        chart_sending_abotie[1] += content['recieved']
        #chart device clic
        '''
        chart_devices_clic[0]  += content['clicsdesktop']
        chart_devices_clic[1]  += content['clicstablet']
        chart_devices_clic[2]  += content['clicsmobile']
        '''
        #chart device open
        chart_devices_open[0]  += content['opensdesktop']
        chart_devices_open[1]  += content['openstablet']
        chart_devices_open[2]  += content['opensmobile']

    context = {
        'pageName' : bdname+' Analyses',
        'bdname' : bdname,
        'chart_open_clic' : chart_open_clic,
        'chart_sending_abotie' : chart_sending_abotie,
        'chart_devices_clic' : chart_devices_open,
        'mail_sending_id' : mail_sending_id
    }
    return render(request, 'AnalyseCompagne.html', context)

def updateGraphContact(request):
    data = {}
    if request.method == 'POST':
        if request.POST.get('chartType') == '1':
            if request.POST.get('mode') == 'Normale':
                if request.POST.get('type') == 'open':
                    nb_open = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/open").where(request.POST.get('device')+"=1 AND mail_sending_id="+request.POST.get('mail_sending_id')).count()
                    #all_open = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/open").where("mail_sending_id="+request.POST.get('mail_sending_id')).count()
                    data = {'nb' : nb_open}
                elif request.POST.get('type') == 'clic':
                    df_clic = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/clic")
                    df_link = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/link")
                    nb_clic=df_clic.alias('c').join(df_link.alias('l'),col('l.id') == col('c.link_id')).where(request.POST.get('device')+"=1 AND mail_sending_id="+request.POST.get('mail_sending_id')).count()
                    data = {'nb' : nb_clic}
            else:
                #Predictive
                pass
        else:
            if request.POST.get('mode') == 'Normale':
                if request.POST.get('type') == 'open':
                    df = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/open").where("mail_sending_id="+request.POST.get('mail_sending_id'))
                    data = {'desktop' : df.where('desktop=1').count(), 'tablet' : df.where('tablet=1').count(), 'mobile' : df.where('mobile=1').count()}
                elif request.POST.get('type') == 'clic':
                    df_clic = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/clic")
                    df_link = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/link")
                    df=df_clic.alias('c').join(df_link.alias('l'),col('l.id') == col('c.link_id')).where("mail_sending_id="+request.POST.get('mail_sending_id'))
                    data = {'desktop' : df.where('desktop=1').count(), 'tablet' : df.where('tablet=1').count(), 'mobile' : df.where('mobile=1').count()}
            elif request.POST.get('mode') == 'Predictive':
                #Predictive
                data = {'desktop' : 0, 'tablet' :0, 'mobile' :0}
                df = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/open").where("mail_sending_id="+request.POST.get('mail_sending_id'))
                if request.POST.get('type') == 'open':
                    for row in df.collect():
                        line = list(row)
                        if model_open_desktop.predict([[line[6], line[3], line[2], line[10], line[12], line[9]]]) == [True]:
                            data['desktop']+=1
                        if model_open_tablet.predict([[line[6], line[3], line[2], line[10], line[9], line[4]]]) == [True]:
                            data['tablet']+=1
                        if model_open_mobile.predict([[line[6], line[3], line[2], line[10], line[12], line[4]]]) == [True]:
                            data['mobile']+=1
                else:
                    for row in df.collect():
                        line = list(row)
                        if model_clic_desktop.predict([[line[6], line[3], line[2], line[10]]]) == [True]:
                            data['desktop']+=1
                        if model_clic_tablet.predict([[line[6], line[3], line[2], line[10]]]) == [True]:
                            data['tablet']+=1
                        if model_clic_mobile.predict([[line[6], line[3], line[2], line[10]]]) == [True]:
                            data['mobile']+=1
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return Http404

def updateGraphCompagne(request):
    if request.POST.get('firstDate') == "" or request.POST.get('secondDate') == "" :
        data = {'error' : '0'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if  datetime.datetime.strptime(request.POST.get('firstDate'), '%Y-%m-%d') > datetime.datetime.strptime(request.POST.get('secondDate'), '%Y-%m-%d') :
        data = {'error' : '1'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    statHour = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/stat_hour").where("mail_sending_id="+request.POST.get('mail_sending_id'))
    if statHour.count() == 0 :
        data = {'error' : '2'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if request.POST.get('action') == 'charge-all-charts' :
        chart_open_clic, chart_sending_recieved,chart_devices_open_clic  = [0, 0], [0, 0], [0, 0, 0]
        for content in  statHour.where("date >= '"+request.POST.get('firstDate')+"' AND date <= '"+request.POST.get('secondDate')+"'").collect():
            if  request.POST.get('mode_sending_recieved') == 'Normale':
                chart_sending_recieved[0] += content['nbmailsend']
                chart_sending_recieved[1] += content['recieved']
            if  request.POST.get('mode_open_clic') == 'Normale':
                chart_open_clic[0] += content["clics"]
                chart_open_clic[1] += content['opens']
            if  request.POST.get('mode_open_clic_devices') == 'Normale':
                if  request.POST.get('type_devices') == 'open':
                    chart_devices_open_clic[0]  += content['opensdesktop']
                    chart_devices_open_clic[1]  += content['openstablet']
                    chart_devices_open_clic[2]  += content['opensmobile']
                else:
                    chart_devices_open_clic[0]  += content['clicsdesktop']
                    chart_devices_open_clic[1]  += content['clicstablet']
                    chart_devices_open_clic[2]  += content['clicsmobile']

            #iCI Predective Model : Remplir list qui est vide en mode Predictive

        data = {'error' : '-1', 'action' : '0', 'data_sending_recieved' : chart_sending_recieved, 'data_open_clic' : chart_open_clic, 'data_devices_open_clic' : chart_devices_open_clic }
    elif request.POST.get('action') == 'charge-open-clic-devices-chart' :
        if request.POST.get('mode') =='Normale':
            if request.POST.get('type') == 'open':
                chart_devices_open = [0, 0, 0]
                for content in  statHour.where("date >= '"+request.POST.get('firstDate')+"' AND date <= '"+request.POST.get('secondDate')+"'").collect():
                    chart_devices_open[0]  += content['opensdesktop']
                    chart_devices_open[1]  += content['openstablet']
                    chart_devices_open[2]  += content['opensmobile']
                data = {'error' : '-1', 'action' : '1', 'open' : True, 'clic' : False, 'data_devices' : chart_devices_open  }
            else:
                chart_devices_clic = [0, 0, 0]
                for content in  statHour.where("date >= '"+request.POST.get('firstDate')+"' AND date <= '"+request.POST.get('secondDate')+"'").collect():
                    chart_devices_clic[0]  += content['clicsdesktop']
                    chart_devices_clic[1]  += content['clicstablet']
                    chart_devices_clic[2]  += content['clicsmobile']
                data = {'error' : '-1', 'action' : '1', 'open' : False, 'clic' : True , 'data_devices' : chart_devices_clic }
        else:
            if request.POST.get('type') == 'open':
                pass
            else:
                pass
    return HttpResponse(json.dumps(data), content_type="application/json")

def globalStat(request, bdname):
    nbComp = 0
    compagnes = []
    for content in spark.read.json("/dataLake/"+bdname+"/mail_sending").select('id', 'name', 'datecreation', "finish").distinct().collect():
        compagnes.append(compagne(content["id"], content["name"], content["datecreation"], content["finish"]))
        nbComp += 1


    nbMailRecieved, nbMailSend , nbMailClic, nbMailOpen, nbMailClic = 0, 0 ,0 ,0, 0
    deb = calendar.timegm(time.gmtime())
    dictOpen = {}
    dictClic = {}
    dictRecieved = {}
    dictSend = {}
    for content in  spark.read.json("/dataLake/"+bdname+"/mail_sending_global_stats").select("uniquclic", "uniqopen", "volumesend", "volumerecieved", "mail_sending_id").collect():
            if content['volumerecieved'] is not None and content['volumesend'] is not None:
                nbMailRecieved += content['volumerecieved']
                #dict Of Recieved
                dictRecieved[content["mail_sending_id"]] = content['volumerecieved']
            if content['volumesend'] is not None:
                nbMailSend += content['volumesend']
                #dict Of Send
                dictSend[content["mail_sending_id"]] = content['volumesend']
            if content['uniqopen'] is not None and  content['volumerecieved'] is not None and content['volumesend'] is not None :
                nbMailOpen += content['uniqopen']
                #dict Of Open
                dictOpen[content["mail_sending_id"]] = content['uniqopen']
            if content['uniquclic'] is not None and content['volumerecieved'] is not None and content['volumesend'] is not None:
                nbMailClic += content['uniquclic']
                #dict Of Clic
                dictClic[content["mail_sending_id"]] = content['uniquclic']

    print(len(dictClic))
    fin = calendar.timegm(time.gmtime())
    print(fin - deb)

    allClientActive= [list(row) for row in  spark.read.json("/dataLake/hub/compte").select("bddname", "active").where("active = true").collect()]
    context = {
        'bdname' : bdname,
        'allClientActive' : allClientActive,
        'nbComp' : nbComp,
        'compagnes' : compagnes,
        'nbMailRecieved' : nbMailRecieved,
        'nbMailSend' : nbMailSend,
        'nbMailOpen' : nbMailOpen,
        'nbMailClic' : nbMailClic,
        'nbMailNotSending' : nbMailSend - nbMailRecieved,
        'dictRecieved' : dictRecieved,
        'dictOpen' : dictOpen,
        'dictClic': dictClic,
        'dictSend' : dictSend,
    }
    return render(request, 'globalStat.html', context)

def updateGlobalStat(request):
    data = {"recieved" : 0, "send" : 0, "open" : 0, "clic" : 0, "error" : "0" }
    if request.POST.get("target") == "stat_hour":
        for content in  spark.read.json("/dataLake/"+request.POST.get("bdname")+"/stat_hour").select("clics", "opens", "nbmailsend", "recieved", "mail_sending_id", "date").where("date >= '"+request.POST.get('firstDate')+"' AND date <= '"+request.POST.get('secondDate')+"'").collect():
            data["recieved"] += content['recieved']
            data["send"] += content['nbmailsend']
            data["open"] += content['opens']
            data["clic"] += content['clics']
    else:
        for content in  spark.read.json("/dataLake/"+request.POST.get("bdname")+"/mail_sending_global_stats").select("uniquclic", "uniqopen", "volumesend", "volumerecieved", "mail_sending_id").collect():
                if content['volumerecieved'] is not None :
                    data["recieved"] += content['volumerecieved']
                if content['volumesend'] is not None:
                    data["send"] += content['volumesend']
                if content['uniqopen'] is not None :
                    data["open"] += content['uniqopen']
                if content['uniquclic'] is not None :
                    data["clic"] += content['uniquclic']

    return HttpResponse(json.dumps(data), content_type="application/json")

def test(request):
    return render(request, 'error.html')

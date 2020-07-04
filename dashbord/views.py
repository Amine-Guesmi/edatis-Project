from django.shortcuts import render, redirect, get_object_or_404
import os, subprocess, json
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMessage,  EmailMultiAlternatives
from django.conf import settings
import logging
import datetime
import subprocess
from django.http import HttpResponse, Http404, JsonResponse
import time
import calendar
from django.template.loader import render_to_string
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

#predict Model par Companes
#send recieved Predictive
model_recieved = pickle.load(open('/home/hduser/machine-Leaning/companes_Model/machineleraingv2Compaine/recievedx.pkl', 'rb'))
#open clic Predictive
model_opens = pickle.load(open('/home/hduser/machine-Leaning/companes_Model/machineleraingv2Compaine/opensx.pkl', 'rb'))
model_clic = pickle.load(open('/home/hduser/machine-Leaning/companes_Model/machineleraingv2Compaine/clicsx.pkl', 'rb'))
#open clic with desk mobile tablet
model_desktopopen = pickle.load(open('/home/hduser/machine-Leaning/companes_Model/machineleraingv2Compaine/M3/opensdesktop(x).pkl', 'rb'))
model_tabletopen = pickle.load(open('/home/hduser/machine-Leaning/companes_Model/machineleraingv2Compaine/M3/openstablet(x).pkl', 'rb'))
model_mobileopen = pickle.load(open('/home/hduser/machine-Leaning/companes_Model/machineleraingv2Compaine/M3/opensmobile(x).pkl', 'rb'))

model_desktopclic = pickle.load(open('/home/hduser/machine-Leaning/companes_Model/machineleraingv2Compaine/M2/clicsdesktop(x).pkl', 'rb'))
model_tabletclic = pickle.load(open('/home/hduser/machine-Leaning/companes_Model/machineleraingv2Compaine/M2/clicstablet(x).pkl', 'rb'))
model_mobileclic = pickle.load(open('/home/hduser/machine-Leaning/companes_Model/machineleraingv2Compaine/M2/clicsmobile(x).pkl', 'rb'))
#recommandation opens
model_recommandation_open = pickle.load(open('/home/hduser/machine-Leaning/recommandation/opens(Tisso).pkl', 'rb'))
#import models
from .models import compte, compagne, Analyse, recommandation, contactAnalyse, IpStats, emailSend
from .forms import recommandationForm
#Spark
import findspark
import pyspark
from pyspark.sql import *
from pyspark.sql.functions import col, year, month, dayofmonth, dayofweek, hour, sum as _sum, max as _max, min as _min
from django.db.models import Sum
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
    dfMailSending = spark.read.json("/dataLake/"+bdname+"/mail_sending")
    dfStatHour = spark.read.json("/dataLake/"+bdname+"/stat_hour")
    df = dfMailSending.join(dfStatHour, dfMailSending.id==dfStatHour.mail_sending_id).select("mail_sending_id", "name", "finish").distinct()
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
    chart_open_clic, chart_devices_clic, chart_devices_open  = [0, 0, 0], [0, 0, 0],[0, 0, 0]
    chart_sending = [0, 0 ,0]
    chart_recieved_inqueue = [0, 0 ,0]
    for content in  statHour.where("mail_sending_id ="+str(mail_sending_id)).collect():
        #chart_open clic
        chart_open_clic[1] += content["opens"]
        chart_open_clic[2] += content['clics']
        #chart sending abotie
        chart_sending[0] += content['nbmailsend']
        chart_recieved_inqueue[1] += content['recieved']
        #chart device clic
        chart_devices_clic[0]  += content['clicsdesktop']
        chart_devices_clic[1]  += content['clicstablet']
        chart_devices_clic[2]  += content['clicsmobile']
        #chart device open
        chart_devices_open[0]  += content['opensdesktop']
        chart_devices_open[1]  += content['openstablet']
        chart_devices_open[2]  += content['opensmobile']
    chart_recieved_inqueue[2] = chart_sending[0] - chart_recieved_inqueue[1];
    chart_open_clic[0] = chart_recieved_inqueue[1]
    context = {
        'pageName' : bdname+' Analyses',
        'bdname' : bdname,
        'chart_open_clic' : chart_open_clic,
        'chart_sending' : chart_sending,
        'chart_recieved_inqueue' : chart_recieved_inqueue,
        'chart_devices_clic' : chart_devices_clic,
        'chart_devices_open' : chart_devices_open,
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
    data = {}
    if request.POST.get('firstDate') == "" or request.POST.get('secondDate') == "" :
        data = {'error' : '0'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if  datetime.datetime.strptime(request.POST.get('firstDate'), '%Y-%d-%m') > datetime.datetime.strptime(request.POST.get('secondDate'), '%Y-%d-%m') :
        data = {'error' : '1'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    statHour = spark.read.json("/dataLake/"+request.POST.get('bdname')+"/stat_hour").where("mail_sending_id="+request.POST.get('mail_sending_id'))
    if statHour.count() == 0 :
        data = {'error' : '2'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if request.POST.get('action') == 'charge-all-charts' :
        chart_open_clic, chart_devices_clic, chart_devices_open  = [0, 0, 0], [0, 0, 0],[0, 0, 0]
        chart_sending = [0, 0 ,0]
        chart_recieved_inqueue = [0, 0 ,0]
        #createDateOfCompane = statHour.where("mail_sending_id ="+request.POST.get('mail_sending_id')).agg(_min("date").alias("date")).select(month("date").alias("month"), year("date").alias("year"), dayofmonth("date").alias("dayofmonth"), dayofweek("date").alias("dayofweek")).collect()[0]
        #lastdate = str(createDateOfCompane["year"])+"-"+str(createDateOfCompane["month"])+"-"+str(createDateOfCompane["dayofmonth"])
        #firstHour = statHour.where("mail_sending_id ="+request.POST.get('mail_sending_id')).where(col("date") == lastdate).agg(_min("hour").alias("hour")).collect()[0]
        #print(firstHour)
        for content in  statHour.where("date >= '"+request.POST.get('firstDate')+"' AND date <= '"+request.POST.get('secondDate')+"'").collect():
            if  request.POST.get('mode_sending_recieved') == 'Normale':
                chart_sending[0] += content['nbmailsend']
                chart_recieved_inqueue[1] += content['recieved']
            else:
                chart_sending[0] += content['nbmailsend']
                chart_recieved_inqueue[1] += int(model_recieved.predict([[content["nbmailsend"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"]]])[0])
            if  request.POST.get('mode_open_clic') == 'Normale':
                chart_open_clic[1]+= content['opens']
                chart_open_clic[2] += content['clics']
            else:
                if  request.POST.get('mode_sending_recieved') != 'Predictive':
                    chart_recieved_inqueue[1] += int(model_recieved.predict([[content["nbmailsend"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"]]])[0])
                chart_open_clic[1] += int(model_opens.predict([[content["nbmailsend"], content["recieved"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["clics"]]]))
                chart_open_clic[2] += int(model_clic.predict([[content["nbmailsend"], content["recieved"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["clics"] ]]))
            if  request.POST.get('mode_open_clic_devices') == 'Normale':
                #chart device clic
                chart_devices_clic[0]  += content['clicsdesktop']
                chart_devices_clic[1]  += content['clicstablet']
                chart_devices_clic[2]  += content['clicsmobile']
                #chart device open
                chart_devices_open[0]  += content['opensdesktop']
                chart_devices_open[1]  += content['openstablet']
                chart_devices_open[2]  += content['opensmobile']
            else:
                chart_devices_clic[0]  += int(model_desktopclic.predict([[content["nbmailsend"], content["recieved"], content["clics"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["opens"]]]))
                chart_devices_clic[1]  += int(model_tabletclic.predict([[content["nbmailsend"], content["recieved"], content["clics"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["opens"] ]]))
                chart_devices_clic[2]  += int(model_desktopopen.predict([[content["nbmailsend"], content["recieved"], content["clics"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["opens"]]]))
                #chart device open
                chart_devices_open[0]  += int(model_desktopopen.predict([[content["nbmailsend"], content["recieved"], content["opens"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["clics"] ]]))
                chart_devices_open[1]  += int(model_tabletopen.predict([[content["nbmailsend"], content["recieved"], content["opens"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["clics"] ]]))
                chart_devices_open[2]  += int(model_mobileopen.predict([[content["nbmailsend"], content["recieved"], content["opens"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["clics"] ]]))
        chart_recieved_inqueue[2] = chart_sending[0] - chart_recieved_inqueue[1];
        chart_open_clic[0] = chart_recieved_inqueue[1]
        data = {'error' : '-1', 'action' : '0', 'chart_sending' : chart_sending, 'chart_recieved_inqueue' : chart_recieved_inqueue, 'chart_open_clic' : chart_open_clic, 'chart_devices_clic' : chart_devices_clic, 'chart_devices_open' : chart_devices_open}
    elif request.POST.get('action') == 'sending-recieved-inqueue' :
        chart_sending = [0, 0 ,0]
        chart_recieved_inqueue = [0, 0 ,0]
        for content in  statHour.where("date >= '"+request.POST.get('firstDate')+"' AND date <= '"+request.POST.get('secondDate')+"'").collect():
            if  request.POST.get('mode') == 'Normale':
                chart_sending[0] += content['nbmailsend']
                chart_recieved_inqueue[1] += content['recieved']
            elif request.POST.get('mode') == 'Predictive':
                chart_sending[0] += content["nbmailsend"]
                chart_recieved_inqueue[1] += int(model_recieved.predict([[content["nbmailsend"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"]]])[0])
        chart_recieved_inqueue[2] = chart_sending[0] - chart_recieved_inqueue[1];
        data = {'error' : '-1', 'action' : '1', 'chart_sending' : chart_sending, 'chart_recieved_inqueue' : chart_recieved_inqueue,}
    elif request.POST.get('action') == 'open-clic' :
        chart_open_clic = [0, 0 ,0]
        for content in  statHour.where("date >= '"+request.POST.get('firstDate')+"' AND date <= '"+request.POST.get('secondDate')+"'").collect():
            if  request.POST.get('mode') == 'Normale':
                chart_open_clic[0] += content['recieved']
                chart_open_clic[1] += content["clics"]
                chart_open_clic[2] += content['opens']
            elif request.POST.get('mode') == 'Predictive':
                chart_open_clic[0] += int(model_recieved.predict([[content["nbmailsend"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"]]])[0])
                chart_open_clic[1] += int(model_clic.predict([[content["nbmailsend"], content["recieved"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["opens"] ]]))
                chart_open_clic[2] += int(model_opens.predict([[content["nbmailsend"], content["recieved"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["clics"]]]))
        data = {'error' : '-1', 'action' : '2', 'chart_open_clic' : chart_open_clic}
    elif request.POST.get('action') == 'charge-open-clic-devices-chart' :
        chart_devices_clic, chart_devices_open  =[0, 0, 0],[0, 0, 0]
        for content in  statHour.where("date >= '"+request.POST.get('firstDate')+"' AND date <= '"+request.POST.get('secondDate')+"'").collect():
            if  request.POST.get('mode') == 'Normale':
                #chart device clic
                chart_devices_clic[0]  += content['clicsdesktop']
                chart_devices_clic[1]  += content['clicstablet']
                chart_devices_clic[2]  += content['clicsmobile']
                #chart device open
                chart_devices_open[0]  += content['opensdesktop']
                chart_devices_open[1]  += content['openstablet']
                chart_devices_open[2]  += content['opensmobile']
            else:
                chart_devices_clic[0]  += int(model_desktopclic.predict([[content["nbmailsend"], content["recieved"], content["clics"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["opens"]]]))
                chart_devices_clic[1]  += int(model_tabletclic.predict([[content["nbmailsend"], content["recieved"], content["clics"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["opens"] ]]))
                chart_devices_clic[2]  += int(model_desktopopen.predict([[content["nbmailsend"], content["recieved"], content["clics"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["opens"]]]))
                #chart device open
                chart_devices_open[0]  += int(model_desktopopen.predict([[content["nbmailsend"], content["recieved"], content["opens"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["clics"] ]]))
                chart_devices_open[1]  += int(model_tabletopen.predict([[content["nbmailsend"], content["recieved"], content["opens"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["clics"] ]]))
                chart_devices_open[2]  += int(model_mobileopen.predict([[content["nbmailsend"], content["recieved"], content["opens"], content["month"], content["hour"], content["dayMonth"], content["dayWeek"], content["clics"] ]]))
            data = {'error' : '-1', 'action' : '3', 'chart_devices_clic' : chart_devices_clic, 'chart_devices_open' : chart_devices_open }
        else:
            pass
    return HttpResponse(json.dumps(data), content_type="application/json")

def globalStat(request, bdname):
    nbComp = 0
    compagnes = []
    stathour = spark.read.json("/dataLake/"+bdname+"/stat_hour")
    mail_sending = spark.read.json("/dataLake/"+bdname+"/mail_sending")
    lstcompIds = []
    for content in mail_sending.join(stathour, mail_sending.id == stathour.mail_sending_id).select('mail_sending_id', 'name', 'datecreation', "finish").distinct().collect():
        compagnes.append(compagne(content["mail_sending_id"], content["name"], content["datecreation"], content["finish"]))
        nbComp += 1
        lstcompIds.append(content["mail_sending_id"])

    nbMailRecieved, nbMailSend , nbMailClic, nbMailOpen, nbMailClic = 0, 0 ,0 ,0, 0
    deb = calendar.timegm(time.gmtime())
    df_globalStat = spark.read.json("/dataLake/"+bdname+"/mail_sending_global_stats")
    dictOpen = {}
    dictClic = {}
    dictRecieved = {}
    dictSend = {}
    devicesDict = {"clic" : [0, 0, 0], "open" : [0, 0, 0]}
    for content in  df_globalStat.where(df_globalStat["mail_sending_id"].isin(lstcompIds)).collect():
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
    devicesDictclic, devicesDictopen = [0, 0, 0], [0, 0 ,0]
    for content in df_globalStat.select("uniqdesktopclic", "uniqdesktopopen", "uniqtabletclic", "uniqtabletopen", "uniqmobileclic", "uniqmobileopen").na.fill(0).collect():
        #Devices CLic
        devicesDictclic[0] += content["uniqdesktopclic"]
        devicesDictclic[1] += content["uniqtabletclic"]
        devicesDictclic[2] += content["uniqmobileclic"]
        #Devices Open
        devicesDictopen[0] += content["uniqdesktopopen"]
        devicesDictopen[1] += content["uniqtabletopen"]
        devicesDictopen[2] += content["uniqmobileopen"]

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
        'devicesDictclic' : devicesDictclic,
        'devicesDictopen' : devicesDictopen
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


#Line Chart Global Stat
def updateStatsPerDate(request):
    df_stathour = spark.read.json("/dataLake/"+request.POST.get("bdname")+"/stat_hour")
    statsPerDate = {"clic" : [] ,"open" : [] , "recieved" : [], "dates" : []}
    # After Loading page
    if request.POST.get("etat") == "0" :
        if  request.POST.get("withCompanes") == "1":
            lstCompanes = list(request.POST.get("companes").split(","))
            df_stats = df_stathour.where(df_stathour["mail_sending_id"].isin(lstCompanes)).groupBy(year("date").alias("year"), month("date").alias("month")).agg(_sum("opens").alias("opens"),_sum("clics").alias("clics"),_sum("recieved").alias("recieved")).orderBy("year", "month")
        else:
            df_stats = df_stathour.groupBy(year("date").alias("year"), month("date").alias("month")).agg(_sum("opens").alias("opens"),_sum("clics").alias("clics"),_sum("recieved").alias("recieved")).orderBy("year", "month")
        for content in df_stats.collect():
            statsPerDate["dates"].append(calendar.month_name[content["month"]]+" "+str(content["year"]))
            statsPerDate["clic"].append(content["clics"])
            statsPerDate["open"].append(content["opens"])
            statsPerDate["recieved"].append(content["recieved"])
    #Actions with listener
    elif request.POST.get("etat") == "1" :
        if request.POST.get("action") == "week" or request.POST.get("action") == "month"  :
            if request.POST.get("action") == "week":
                nbday = 7
            else:
                nbday = 30
            if  request.POST.get("withCompanes") == "1":
                lstCompanes = list(request.POST.get("companes").split(","))
                maxDateInStatHour =  (datetime.datetime.strptime(df_stathour.where(df_stathour["mail_sending_id"].isin(lstCompanes)).agg(_max("date").alias("date")).collect()[0]["date"], "%Y-%m-%d") - datetime.timedelta(days=nbday)).strftime("%Y-%m-%d")
                df_stats =  df_stathour.where(df_stathour["mail_sending_id"].isin(lstCompanes)).where("date >'"+maxDateInStatHour+"'").groupBy(year("date").alias("year"), month("date").alias("month"), dayofmonth("date").alias("day")).agg(_sum("opens").alias("opens"),_sum("clics").alias("clics"),_sum("recieved").alias("recieved")).orderBy("year", "month", "day")
            else:
                maxDateInStatHour =  (datetime.datetime.strptime(df_stathour.agg(_max("date").alias("date")).collect()[0]["date"], "%Y-%m-%d") - datetime.timedelta(days=nbday)).strftime("%Y-%m-%d")
                df_stats =  df_stathour.where("date >'"+maxDateInStatHour+"'").groupBy(year("date").alias("year"), month("date").alias("month"), dayofmonth("date").alias("day")).agg(_sum("opens").alias("opens"),_sum("clics").alias("clics"),_sum("recieved").alias("recieved")).orderBy("year", "month", "day")

            for content in df_stats.collect():
                statsPerDate["dates"].append(str(content["day"])+" "+calendar.month_name[content["month"]])
                statsPerDate["clic"].append(content["clics"])
                statsPerDate["open"].append(content["opens"])
                statsPerDate["recieved"].append(content["recieved"])
        elif request.POST.get("action") == "sixMonth" :
            if  request.POST.get("withCompanes") == "1":
                lstCompanes = list(request.POST.get("companes").split(","))
                maxDateInStatHour =  (datetime.datetime.strptime(df_stathour.where(df_stathour["mail_sending_id"].isin(lstCompanes)).agg(_max("date").alias("date")).collect()[0]["date"], "%Y-%m-%d") - datetime.timedelta(days=180)).strftime("%Y-%m-%d")
                df_stats = df_stathour.where(df_stathour["mail_sending_id"].isin(lstCompanes)).where("date >'"+maxDateInStatHour+"'").groupBy(year("date").alias("year"), month("date").alias("month")).agg(_sum("opens").alias("opens"),_sum("clics").alias("clics"),_sum("recieved").alias("recieved")).orderBy("year", "month")
            else:
                maxDateInStatHour =  (datetime.datetime.strptime(df_stathour.agg(_max("date").alias("date")).collect()[0]["date"], "%Y-%m-%d") - datetime.timedelta(days=180)).strftime("%Y-%m-%d")
                df_stats = df_stathour.where("date >'"+maxDateInStatHour+"'").groupBy(year("date").alias("year"), month("date").alias("month")).agg(_sum("opens").alias("opens"),_sum("clics").alias("clics"),_sum("recieved").alias("recieved")).orderBy("year", "month")
            for content in df_stats.collect():
                statsPerDate["dates"].append(calendar.month_name[content["month"]]+" "+str(content["year"]))
                statsPerDate["clic"].append(content["clics"])
                statsPerDate["open"].append(content["opens"])
                statsPerDate["recieved"].append(content["recieved"])
    elif  request.POST.get("etat") == "2" :
        pass
    return HttpResponse(json.dumps(statsPerDate), content_type="application/json")

def getNewDataOfPredictiveComp():
    NumberOfcomp =recommandation.objects.count()
    if NumberOfcomp != 0:
        recom_Analyse = recommandation.objects.aggregate(Sum('sent'), Sum('recieved'), Sum('clics'), Sum('opens'))
        in_queue = recom_Analyse["sent__sum"] - recom_Analyse["recieved__sum"]
        return {"recommandation" :  recommandation.objects.all(), "compNumber" : recommandation.objects.count(), "clics" : recom_Analyse["clics__sum"] , "opens" : recom_Analyse["opens__sum"] , "recieved" : recom_Analyse["recieved__sum"] , "sent" : recom_Analyse["sent__sum"] , "in_queue" : in_queue  }
    else:
        return {"recommandation" :  None, "compNumber" : 0, "clics" : 0 , "opens" : 0 , "recieved" : 0 , "sent" : 0 , "in_queue" : 0  }
def recommandationFuntion(request):
    allAnalyseDict = getNewDataOfPredictiveComp()
    dataPerTimes = recommandation.objects.values('dateRecomendation').order_by('dateRecomendation').annotate(clics=Sum('clics'), opens=Sum('opens'), recieved=Sum('recieved'))
    labels, clics, opens, recieved = [], [], [], []
    for dataPerTime in dataPerTimes:
        recieved.append(dataPerTime["recieved"])
        clics.append(dataPerTime["clics"])
        opens.append(dataPerTime["opens"])
        dateRec = dataPerTime["dateRecomendation"].split("-")
        labels.append(str(dateRec[2]+" "+(calendar.month_name[int(dateRec[1])])+" "+dateRec[0]))
    context = {
        'recommandation' : allAnalyseDict["recommandation"],
        'compNumber' : allAnalyseDict["compNumber"],
        'clics' : allAnalyseDict["clics"],
        'opens' : allAnalyseDict["opens"],
        'recieved' : allAnalyseDict["recieved"],
        'sent' :  allAnalyseDict["sent"],
        'in_queue' : allAnalyseDict["in_queue"],
        'recievedList' : recieved,
        'clicsList' :  clics,
        'opensList' :  opens,
        'labels' :  labels
    }
    return render(request, 'recommandation.html', context)

def recommandationAction(request):
    dateCreation = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
    recieved = int(model_recieved.predict([[request.POST.get("compSent"), dateCreation.month, request.POST.get("hour"), dateCreation.day, (dateCreation.weekday() + 1)]])[0])
    df_globalStat = spark.read.json("/dataLake/Tisseo/mail_sending_global_stats")
    nearnbSend = (df_globalStat.where("volumesend <= "+str(request.POST.get("compSent"))).agg(_max("volumesend").alias("nbMailSend")).collect())[0][0]
    bestClic = (df_globalStat.where("volumesend = "+str(nearnbSend)).collect())[0][1]
    opens = int(model_opens.predict([[request.POST.get("compSent"), recieved, dateCreation.month, request.POST.get("hour"), dateCreation.day, (int(dateCreation.weekday()) + 1), bestClic]]))
    clics = int(model_clic.predict([[request.POST.get("compSent"), recieved, dateCreation.month, request.POST.get("hour"), dateCreation.day , (int(dateCreation.weekday()) + 1), opens ]]))
    data = {'data_sent_recieved_inqueue' : [request.POST.get("compSent"), recieved, (int(request.POST.get("compSent")) - recieved)], "data_open_clic" : [request.POST.get("compSent"), opens, clics]}
    if request.POST.get("databaseSave") == "1" :
        if request.method == "POST":
            obj = {'user' : request.user,'compName' : request.POST.get('compName'),'sent' : request.POST.get('compSent'),'recieved' : recieved,'opens' : opens,'clics' : clics,'dateRecomendation' : request.POST.get('date') ,'hour' : request.POST.get('hour')}
            recom = recommandationForm(obj)
            recom.save()
            recom_Analyse = recommandation.objects.aggregate(Sum('sent'), Sum('recieved'), Sum('clics'), Sum('opens'))
            data["sent"] = recom_Analyse["sent__sum"]
            data["recieved"] = recom_Analyse["recieved__sum"]
            data["clics"] = recom_Analyse["clics__sum"]
            data["opens"] = recom_Analyse["opens__sum"]
            data["in_queue"] = recom_Analyse["sent__sum"] - recom_Analyse["recieved__sum"]
            data["nbComp"] = recommandation.objects.count()
            data['comp_list'] = render_to_string('ajax_template_dashbord/listCompagnes.html',{'recommandation' : recommandation.objects.all()}, request=request)
            dataPerTimes = recommandation.objects.values('dateRecomendation').order_by('dateRecomendation').annotate(clics=Sum('clics'), opens=Sum('opens'), recieved=Sum('recieved'))
            labels, clicsLst, opensLst, recievedLst = [], [], [], []
            for dataPerTime in dataPerTimes:
                recievedLst.append(dataPerTime["recieved"])
                clicsLst.append(dataPerTime["clics"])
                opensLst.append(dataPerTime["opens"])
                dateRec = dataPerTime["dateRecomendation"].split("-")
                labels.append(str(dateRec[2]+" "+(calendar.month_name[int(dateRec[1])])+" "+dateRec[0]))
            data["recievedLst"] = recievedLst
            data["clicsLst"] = clicsLst
            data["opensLst"] = opensLst
            data["labels"] = labels
    return HttpResponse(json.dumps(data), content_type="application/json")
def recommandationCompDetails(request, id):
    if request.method == "GET":
        comp = get_object_or_404(recommandation, id=id)
        print(comp.clics, comp.sent)
        data= {"compName" : comp.compName, 'sent' : comp.sent, 'clics' : comp.clics, 'opens' : comp.opens, "recieved" : comp.recieved}
        return JsonResponse(data)
    else:
        return Http404
def recommandationDelete(request, id):
    if request.method == "GET":
        recommandation.objects.get(id=id).delete()
        dataPerTimes = recommandation.objects.values('dateRecomendation').order_by('dateRecomendation').annotate(clics=Sum('clics'), opens=Sum('opens'), recieved=Sum('recieved'))
        labels, clics, opens, recieved = [], [], [], []
        for dataPerTime in dataPerTimes:
            recieved.append(dataPerTime["recieved"])
            clics.append(dataPerTime["clics"])
            opens.append(dataPerTime["opens"])
            dateRec = dataPerTime["dateRecomendation"].split("-")
            labels.append(str(dateRec[2]+" "+(calendar.month_name[int(dateRec[1])])+" "+dateRec[0]))
        analyseSum = getNewDataOfPredictiveComp()
        data = {"compNumber" : analyseSum["compNumber"], "clics" : analyseSum["clics"] , "opens" : analyseSum["opens"] , "recieved" : analyseSum["recieved"] , "sent" : analyseSum["sent"] , "in_queue" : analyseSum["in_queue"],  "comp_list" : 0}
        data["comp_list"] = render_to_string('ajax_template_dashbord/listCompagnes.html',{'recommandation' : recommandation.objects.all()}, request=request)
        data["recievedLst"] = recieved
        data["clicsLst"] = clics
        data["opensLst"] = opens
        data["labels"] = labels
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return Http404
def recommandationDeleteModal(request, id):
    if request.method == "GET":
        data = {}
        data['html_modal'] = render_to_string('ajax_template_dashbord/deleteComp.html',{'comp' : get_object_or_404(recommandation, id=id)}, request=request)
        return JsonResponse(data)
    else:
        return Http404
def allContact(request, bdname, mail_sending_id):
    df_mail_sending_resum_trans = spark.read.json("/dataLake/"+bdname+"/mail_sending_resume_trans/dataAnalyse")
    nbSent , clics, opens, bounce, contactList =0 ,0 ,0, 0, []
    for content in df_mail_sending_resum_trans.where("mail_sending_id = "+str(mail_sending_id)).na.fill(0).collect():
        opens +=content["open"]
        clics +=content["clic"]
        bounce += int(content["bounce"])
        nbSent += 1
        contactList.append(contactAnalyse(mail_sending_id, content["email"], content["clic"], content["open"], content["bounce"]))
    context = {
        "opens" : opens,
        "clics" : clics,
        "sent" : nbSent,
        "recieved" : nbSent - bounce,
        "contactList" : contactList,
        'inqueue' : nbSent - (nbSent - bounce),
        'numBounce' : bounce ,
        "mail_sending_id" : mail_sending_id,
        "dbname" : bdname
    }
    return render(request, "allContact.html", context)
def AnalyseIps(request, dbname):
    df_ip_contact = spark.read.json("/dataLake/"+dbname+"/ipContact")
    df_ip_action = spark.read.json("/dataLake/"+dbname+"/ipActions")
    ip_contact_dict = {"ip" : [], "nbContact" : []}
    for content in df_ip_contact.collect():
        PosClearIp = content["ip"].index("_",3) + 1
        ip_contact_dict["ip"].append(content["ip"][PosClearIp:])
        ip_contact_dict["nbContact"].append(content["nbContact"])
    labelsList, opensList, clicsList, bounceList = [], [], [], []
    for content in df_ip_action.collect():
        PosClearIp = content["ip"].index("_",3) + 1
        labelsList.append(content["ip"][PosClearIp:])
        opensList.append(content["opens"])
        clicsList.append(content["clics"])
        bounceList.append(content["Bounce"])
    numberContact, NumberIp, sumOpens, sumClics, sumBounce, sumSent = 0, 0 ,0 ,0 ,0 ,0
    for content in spark.read.json("/dataLake/Tisseo/dataIpsGlobalStats").collect():
        numberContact = content["NumberContact"]
        NumberIp = content["NumbeIP"]
        sumOpens = content["sumOpens"]
        sumClics = content["sumClics"]
        sumBounce = content["sumBounce"]
        sumSent = content["sumSent"]
    sumRecieved = sumSent - sumBounce

    context = {
        "numberContact" : numberContact,
        "NumberIp" : NumberIp,
        "sumOpens" : sumOpens,
        "sumClics" : sumClics,
        "sumBounce" : sumBounce,
        "sumSent" : sumSent,
        "sumRecieved" : sumRecieved ,
        "labelsList" : labelsList ,
        "opensList" : opensList ,
        "clicsList" : clicsList,
        "bounceList" : bounceList,
        "labelsIpContact" : ip_contact_dict["ip"] ,
        "nbContact" : ip_contact_dict["nbContact"]
    }
    return render(request, "IpsAnalyse.html", context)

def getMailIpsStats(request):
    df_all_analyse = spark.read.json("/dataLake/Tisseo/dataIps")
    lstAllAnalyse = []
    for content in df_all_analyse.collect():
        PosClearIp = content["ip"].index("_",3) + 1
        lstAllAnalyse.append({"email" : content["email"], "ip" : content["ip"][PosClearIp:], "clics" :  content["clics"], "opens" : content["opens"], "bounce" : content["bounce"]})
    return JsonResponse(lstAllAnalyse, safe=False)
def sendStatsMail(request):
    mailList = []
    for  content in request.POST.get("mails").split(","):
        if (content.index("@gmail.com") != -1)  or  (content.index(".org") != -1) :
            mailList.append(content)
    objects =  json.loads(request.POST.get("rates"))
    allObjects = []
    for content in range(0, len(objects["dict"])):
        allObjects.append(emailSend(objects["dict"][content][2],objects["dict"][content][3],objects["dict"][content][1]))
    subject, from_email, to = 'hello', settings.EMAIL_HOST_USER , mailList
    text_content = 'This is an important message.'
    html_content = render_to_string("ajax_template_dashbord/sendingMail.html", {"objectEmailClassification" : allObjects, "top" : objects["top"], "type" : objects["type"], "date" : datetime.datetime.today().strftime('%Y-%m-%d')  })
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return JsonResponse({"status": True})
def test(request):
    return render(request, 'error.html')

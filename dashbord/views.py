from django.shortcuts import render
import os, subprocess, json
import logging

from .models import compte

#logger instance
logger = logging.getLogger(__name__)

# Create your views here.
def dashbord(request):
    content =subprocess.Popen(["hdfs", "dfs", "-cat", "/dataLake/hub/compte/*.json"], stdout=subprocess.PIPE)
    comptes = []

    for line in content.stdout:
        jsonTranform = json.loads(line)
        comptes.append(compte(jsonTranform['id'],  jsonTranform['name'], jsonTranform['bddname'], jsonTranform['active'], jsonTranform['dateinscription']))

    context = {
        'comptes' :  comptes
    }
    return render(request, 'dashbord.html', context)

from django.shortcuts import render
import os, subprocess

# Create your views here.
def dashbord(request):
    content =subprocess.Popen(["hdfs", "dfs", "-cat", "/dataLake/Tisseo/open/*.json"], stdout=subprocess.PIPE)
    context = {
        'content' : content.stdout
    }
    return render(request, 'dashbord.html', context)

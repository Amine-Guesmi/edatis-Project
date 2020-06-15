from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class recommandation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    compName = models.CharField(max_length=50)
    sent = models.IntegerField()
    recieved = models.IntegerField()
    opens = models.IntegerField()
    clics = models.IntegerField()
    clicDesktop = models.IntegerField()
    clictablet = models.IntegerField()
    clicMobile = models.IntegerField()
    openDesktop = models.IntegerField()
    openTablet = models.IntegerField()
    openMobile = models.IntegerField()
    created = models.DateTimeField(default=timezone.now())
    dateRecomendation =  models.CharField(max_length=50)



class compte:
    def __init__(self, id, name, bddname, active, inscriptiondate):
        self.id = id
        self.name = name
        self.bddname = bddname
        self.active = active
        self.inscriptiondate = inscriptiondate

class compagne:
    def __init__(self, id, name, finish):
        self.id = id
        self.name = name
        self.finish = finish
    def __init__(self, id, name, datecreation, finish):
        self.id = id
        self.name = name
        self.datecreation = datecreation
        self.finish = finish


class Analyse:
    def __init__(self, tablet_open, tel_open, Desktop_open, SumAllDevicesOpen, SumAllDevicesClic, nbMailSending):
        self.nbMailSending = nbMailSending
        self.tablet_open = tablet_open
        self.tel_open = tel_open
        self.Desktop_open = Desktop_open
        self.SumAllDevicesOpen = SumAllDevicesOpen
        self.SumAllDevicesClic = SumAllDevicesClic

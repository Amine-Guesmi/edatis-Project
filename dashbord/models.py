from django.db import models

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

class Analyse:
    def __init__(self, tablet_open, tel_open, Desktop_open, SumAllDevices):
        self.tablet_open = tablet_open
        self.tel_open = tel_open
        self.Desktop_open = Desktop_open
        self.SumAllDevices = SumAllDevices
    

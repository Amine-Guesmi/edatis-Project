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

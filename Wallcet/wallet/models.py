from django.db import models

# Create your models here.


 
class Wallet(models.Model):
    eMail = models.CharField(max_length=200, blank= False, null=False, default='')
    contrasenia  = models.CharField(max_length=200, blank= False, null=False, default='')

class Cuenta(models.Model):
    walle = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    llavePrivada = models.CharField(max_length=200, blank= False, null=False, default='')
    llavePublica = models.CharField(max_length=200, blank= False, null=False, default='')
    balance = models.IntegerField('Balance', blank = False, null = False)

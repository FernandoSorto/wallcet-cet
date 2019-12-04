from django import forms
from django.forms import TextInput
from .models import Cuenta, Wallet
 
class nuevaWalletForm(forms.ModelForm):
     class Meta:
         model = Wallet
         fields = [
             'eMail',
             'contrasenia',
         ]
         labels = {
             'eMail': 'Email',
             'contrasenia': 'Contrasenia',
         }

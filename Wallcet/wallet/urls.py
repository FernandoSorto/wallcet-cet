from django.urls import path
from django.conf.urls import url

from . import views

app_name='walletApp'

urlpatterns = [
    path('', views.index, name='paginaPrincipal'),
    path('home/', views.home, name='paginaHome'),
    
]

from django.urls import path
from .import views

app_name = 'login'

urlpatterns = [
  path('', views.login, name="login"),
  path('logar', views.logar, name="logar"),
  path('log_out', views.log_out, name='log_out'),
  
]

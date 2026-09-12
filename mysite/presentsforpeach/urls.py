from django.urls import path 
from . import views 

app_name = "presentsforpeach"

urlpatterns = [
    path("", views.login, name="login"),
    
    
    
    
    
    
    path("underconstruction", views.showUnderConstruction, name="underconstruction")
]
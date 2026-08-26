from django.urls import path 

from . import views

app_name = "main"

urlpatterns = [
    path("", views.mainHome, name="mainHome"),
    
    # paths for about, contact, and recruiters
    path("about", views.AboutView.as_view(), name="about-view"),    
    
]
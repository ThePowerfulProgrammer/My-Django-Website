from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import date

# Views 

# 1) Present a client with a login page
def login(request):
    if request.method == "POST":
        #  are you my peach?
        peach = User.objects.get(username="test")
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None and peach == user:
            print("FOUND YOU PEACH")
            
            return redirect("presentsforpeach:underconstruction")
        else:
            
            return redirect("main:mainHome")        
    else:        
        return render(request, "presentsforpeach/login.html", context={})    
     


# 2) Temp Under Construction Page
def showUnderConstruction(request):
    scheduleReleaseDate = date(2026, 10, 30)
    today = date.today()
    
    print(scheduleReleaseDate)
    print(today)
    print(scheduleReleaseDate - today)
    
    
    return render(request, "presentsforpeach/underconstruction.html", context={})
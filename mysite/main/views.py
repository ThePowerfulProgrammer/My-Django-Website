from django.shortcuts import render
from django.views import View

# Create your views here.


def mainHome(request):
    
    return render(request, "main/mainHome.html", context={})


# About VIEW
class AboutView(View):
    
    print("IN about ")
    
        
    def get(self, request):
        print("RENDER TEMPLATE")
        return render(request, "main/about.html", context={})
    
    
    
# what am I up to 
def page(request):
    # If I had a  model I can include data about my current pursuits
    return render(request, "main/page.html", context={})
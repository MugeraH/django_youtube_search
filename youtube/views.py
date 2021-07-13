from django.shortcuts import render



def Home(request):
    ctx={}
    return render(request,"home.html",ctx)

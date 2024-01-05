
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    return render(request,"index.html")

def room(request):
    return render(request,"chat.html")
    #return render(request, "room.html", {"room_name": room_name})


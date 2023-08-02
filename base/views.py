from django.shortcuts import render

from .models import Room, Topic, Message, User, BlogPost

def login(request):
    pass

def logout(request):
    pass

def register(request):
    pass

def userProfile(request, pk):
    pass

def updateUser(request):
    pass

def home(request):
    return render(request, "base/home.html")

def room(request, pk):
    return render(request, "base/room.html")

def createRoom(request):
    pass

def updateRoom(request, pk):
    pass

def deleteRoom(request, pk):
    pass

def deleteMessage(request, pk):
    pass

def createPost(request):
    pass

def updatePost(request):
    pass

def deletePost(request):
    pass

def listTopics(request):
    pass

def showActivity(request):
    pass
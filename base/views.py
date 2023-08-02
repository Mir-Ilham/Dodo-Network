from django.shortcuts import render, redirect

from .models import Room, Topic, Message, User, BlogPost
from .forms import RoomForm

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
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, "base/room_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

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
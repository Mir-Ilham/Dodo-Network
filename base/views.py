from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Room, Topic, Message, User, BlogPost
from .forms import RoomForm, PostForm

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
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
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
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, "base/post_form.html", context)

def updatePost(request, pk):
    post = BlogPost.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/post_form.html', context)

def deletePost(request, pk):
    post = BlogPost.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': post})

def listTopics(request):
    pass

def showActivity(request):
    pass
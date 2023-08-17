from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Room, Topic, Message, User, BlogPost
from .forms import RoomForm, PostForm, MyUserCreationForm, UserForm, UpdateUserForm

def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")
        else:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Username OR password incorrect")
    
    context = {"page": page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
    context = {"form": form}
    return render(request, "base/login_register.html", context)

@login_required(login_url="login")
def userProfile(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    viewRooms = False
    if q == 'rooms':
        viewRooms = True
    user = User.objects.get(id=pk)
    connections = user.connections.all()
    rooms = user.room_set.all()
    skills = user.experts.all()
    room_messages = user.message_set.all()
    posts = user.blogpost_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms": rooms, "room_messages": room_messages, 
               "topics": topics, "posts": posts, "viewRooms": viewRooms, 
               'skills': skills, 'pk': pk, 'connections': connections}
    return render(request, "base/profile.html", context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update-user.html', context)

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()[0:7]
    room_count = rooms.count()
    room_messages = []
    connections = request.user.connections.all()

    for connection in connections:
        for message in connection.message_set.all()[0:2]:
            room_messages.append(message)

    context = {"rooms": rooms, "topics": topics, "room_count": room_count, "room_messages": room_messages}
    return render(request, "base/home.html", context)

@login_required(login_url="login")
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    participants = room.participants.all()
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    
    context = {'form': form, 'topics': topics}
    return render(request, "base/room_form.html", context)

@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return redirect('home')
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return redirect('home')
    
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url="login")
def createPost(request):
    form = PostForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        BlogPost.objects.create(
            author = request.user,
            title = request.POST.get('title'),
            content = request.POST.get('content'),
            topic = topic
        )
        return redirect('user-profile', pk=request.user.id)
    
    context = {'form': form, 'topics': topics}
    return render(request, "base/post_form.html", context)

@login_required(login_url="login")
def updatePost(request, pk):
    post = BlogPost.objects.get(id=pk)
    form = PostForm(instance=post)
    topics = Topic.objects.all()

    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.topic = topic
        post.save()
        return redirect('user-profile', pk=request.user.id)
    context = {'form': form, 'topics': topics, 'post': post}
    return render(request, 'base/post_form.html', context)

@login_required(login_url="login")
def deletePost(request, pk):
    post = BlogPost.objects.get(id=pk)

    if request.user != post.author:
        return redirect('home')

    if request.method == "POST":
        post.delete()
        return redirect('user-profile', pk=request.user.id)
    
    return render(request, 'base/delete.html', {'obj': post})

@login_required(login_url='login')
def addSkill(request, pk):
    user= User.objects.get(id=pk)
    topics = Topic.objects.all()

    if request.user != user:
        return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        topic.experts.add(request.user)
        return redirect('user-profile', pk=pk)
    
    context = {'topics': topics}
    return render(request, "base/add_skill.html", context)

@login_required(login_url='login')
def connect(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()

    if request.user == user:
        return redirect('home')
    
    request.user.connections.add(user)

    return redirect('user-profile', pk=user.id)

@login_required(login_url='login')
def listTopics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

@login_required(login_url='login')
def showActivity(request):
    room_messages = []
    connections = request.user.connections.all()

    for connection in connections:
        for message in connection.message_set.all():
            room_messages.append(message)

    context = {"room_messages": room_messages}
    return render(request, 'base/activity.html', context)
from django.shortcuts import render ,HttpResponse  ,redirect
from django.contrib.auth  import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.db.models import Q
from base.models import Room , Topic , Message
from base.forms import RoomForm , UserForm




#  Create your views here.

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , 'An error occurred durign registration!')
    
    context = {'form':form}
    return render(request, 'base/login_register.html' , context)


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try : 
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist!")

        user = authenticate(request , username=username , password = password)
        if user is not None:
            login(request ,user)
            return redirect('home')
        else :
            messages.error(request, "Username OR Password does not exist")


    context = {'page':page}
    return render(request ,'base/login_register.html' , context)



def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') 
    if q is None:
        q = ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)

        )

    topics = Topic.objects.all()[:5]
    room_counts = rooms.count()

    #to display the recent activity
    room_messages = Message.objects.filter(room__name__icontains=q)

    context={'rooms':rooms , 'topics':topics , 
             'room_counts':room_counts , 'room_messages':room_messages}
    return render(request, 'base/home.html' ,context )



def room(request ,pk):# here pk = primary key to identify the room
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created') # message_set will give us all children of the room
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room' , pk=room.id)

    context = {'room' : room , 
        'room_messages':room_messages ,'participants':participants}
    return render(request ,'base/room.html' ,context)

def userProfile(request , pk):# here pk = primary key to identify the user
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()

    # to display the recent activity
    room_messages = user.message_set.all()
    
    # to display the Topics
    topics = Topic.objects.all()


    context = {'user':user , 'rooms':rooms ,
        'room_messages':room_messages , 'topics':topics}
    return render(request , 'base/profile.html' ,context)

@login_required(login_url='login')
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)
        # https://youtu.be/PtQiiknWUcI?t=18365  to understand get_of_create() working

        # print("\n\n" ,topic,"\n\n" , created,"\n\n")
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )

        return redirect('home')

    context = {'form':form , 'name':'Create','topics':topics}
    return render(request , 'base/room_form.html' ,context)

@login_required(login_url='login')
def updateRoom(request , pk):# here pk = primary key to identify the room
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    # condition to prevent that other user can not edit the other user's room
    if request.user != room.host:
        return HttpResponse('You are not allowed!!')


    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context={'form':form , 'name':'Update' ,'topics':topics , 'room':room}
    return render(request , 'base/room_form.html' ,context)

@login_required(login_url='login')
def deleteRoom(request , pk):# here pk = primary key to identify the room
    room = Room.objects.get(id=pk)

    # condition to prevent that other user can not delete the other user's room
    if request.user != room.host:
        return HttpResponse('You are not allowed!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request , 'base/delete.html' ,{'obj':room})



@login_required(login_url='login')
def deleteMessage(request , pk):# here pk = primary key to identify the message
    message = Message.objects.get(id=pk)

    # condition to prevent that other user can not delete the other user's room
    if request.user != message.user:
        return HttpResponse('You are not allowed!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request , 'base/delete.html' ,{'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST , instance=user)
        if form.is_valid():
            form.save()
            # print()
            # print(request.META.get("HTTP_REFERER"))
            # print()
            return redirect('user-profile' , pk=user.id)

    context = {'form':form}
    return render(request , 'base/update_user.html',context)


def topics(request):
    return render(request , 'base/topics.html')



def topicsPage(request):
    q = request.GET.get('q') 
    if q is None:
        q = ''

    topics = Topic.objects.filter(name__icontains=q)[:5]
    return render(request , 'base/topics_page.html' ,{'topics':topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request , 'base/activity_page.html' , {'room_messages':room_messages})
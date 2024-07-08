from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Message, Chat
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/login/')
def index(request):
  if request.method == 'POST':
    print("Revived Data: " + request.POST['textmessage'])
    testChat = Chat.objects.get(id=1) 
    # create ein neues object vom Typ Message. 
    Message.objects.create(text=request.POST['textmessage'], chat=testChat, author=request.user, receiver=request.user)
  chatMessages = Message.objects.filter(chat__id=1)    
  return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    redirect_url = request.GET.get('next', '/chat/')
    
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect(request.POST.get('redirect', redirect_url))
        else:
            messages.error(request, 'Falsche Userdaten')
            return render(request, 'auth/login.html', {'wrongPasswort': True, 'redirect': redirect_url})
    
    return render(request, 'auth/login.html', {'redirect': redirect_url})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Der Benutzername ist bereits vergeben')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Diese E-Mail-Adresse wird bereits verwendet')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('/login/')
        else:
            messages.error(request, 'Die Passwörter stimmen nicht überein')
    
    return render(request, 'auth/register.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')
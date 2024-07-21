import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import Message, Chat
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers

@login_required(login_url='/login/')
def index(request):
  if request.method == 'POST':
    print("Revived Data: " + request.POST['textmessage'])
    testChat = Chat.objects.get(id=1) 
    # create ein neues object vom Typ Message. 
    new_message =  Message.objects.create(text=request.POST['textmessage'], chat=testChat, author=request.user, receiver=request.user)
    serialized_obj = serializers.serialize('json', [ new_message ])
    # Statt das serialisierte Objekt als String zurückzugeben, parsen wir es zuerst zu einem Python-Objekt
    serialized_obj = serializers.serialize('json', [new_message])
    serialized_obj = json.loads(serialized_obj)[0]['fields']  # Nimm das erste Element aus der Liste
    print(serialized_obj)
    return JsonResponse(serialized_obj, safe=False)
  chatMessages = Message.objects.filter(chat__id=1)    
  return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    redirect = request.GET.get('next', '/chat')
    if request.method == 'POST':
       user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
       if user:
          login(request, user)
          return HttpResponseRedirect(request.POST.get('redirect'))
       else:
          print('user wrong')
          messages.success(request, 'Falsche Userdaten')
          return render(request, 'auth/login.html', {'wrongPasswort': True, 'redirect': redirect})
       
    return render(request, 'auth/login.html', {'redirect': redirect})

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
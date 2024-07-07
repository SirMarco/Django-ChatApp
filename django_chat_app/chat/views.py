from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

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
    redirect = request.GET.get('next')
    if request.method == 'POST':
       user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
       if user:
          login(request, user)
          return HttpResponseRedirect(request.POST.get('redirect'))
       else:
          print('user wrong')
          return render(request, 'auth/login.html', {'wrongPasswort': True, 'redirect': redirect})
       
    return render(request, 'auth/login.html', {'redirect': redirect})


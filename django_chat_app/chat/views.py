from django.shortcuts import render
from .models import Message, Chat

def index(request):
  if request.method == 'POST':
    print("Revived Data: " + request.POST['textmessage'])
    testChat = Chat.objects.get(id=1) 
    # create ein neues object vom Typ Message. 
    Message.objects.create(text=request.POST['textmessage'], chat=testChat, author=request.user, receiver=request.user)
  chatMessages = Message.objects.filter(chat__id=1)    
  return render(request, 'chat/index.html', {'messages': chatMessages})

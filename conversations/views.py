from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from conversations.models import Conversation

@login_required
def dash(request):
  context = {}

  context['conversations'] = Conversation.objects.all()

  return render(request, 'dash.html', context)

@login_required
def chat(request, conversation_id):
  context = {}

  context['conversation'] = Conversation.objects.get(pk=conversation_id)

  return render(request, 'chat.html', context)

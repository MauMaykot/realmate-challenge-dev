from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dash(request):
  context = {}

  return render(request, 'dash.html', context)

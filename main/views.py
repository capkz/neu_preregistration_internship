from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404

def home(request):
    return render(request, 'main/home.html', {'nbar': 'home'})
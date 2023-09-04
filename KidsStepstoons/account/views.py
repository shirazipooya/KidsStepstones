from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from .models import User

@login_required
def home(request):
    return render(request, "registration/home.html")



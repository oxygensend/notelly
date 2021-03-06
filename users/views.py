from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from notes.models import Topic
from .models import CustomUser
from .forms import CustomUserCreationForm

def register(request):
    """ New user registration """

    if request.method != 'POST':
        form = CustomUserCreationForm
    else:
        form = CustomUserCreationForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            new_login = form.save()
            login(request, new_login)
            return redirect('notes:index')
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)



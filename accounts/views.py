from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users
# Create your views here.
from .forms import CreateUserForm

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('edatis_dashbord:dashbord')
        else:
            messages.warning(request, 'Username Or Password is incorrect')
    context = {}
    return render(request, 'login.html', context)

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='waiter')
                user.groups.add(group)
                messages.success(request, 'Account was created for ' + username)
                return redirect('accounts:login')
    context = {
        'form' : form
    }
    return render(request, 'register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('accounts:login')

def error403(request):
    return render(request, 'permessionDenied.html')

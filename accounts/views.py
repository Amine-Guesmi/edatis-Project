from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from .forms import CreateUserForm
from django.http import JsonResponse
from django.template.loader import render_to_string

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if (list(user.groups.values_list('name',flat = True)) == ['admin']):
                    return redirect('edatis_dashbord:allUsers')
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

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['waiter'])
def error403(request):
    return render(request, 'permessionDenied.html')

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def save_all(request, form, template_name, etat):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            if etat:
                group = Group.objects.get(name=request.POST.get('role'))
                user.groups.add(group)
            else:
                group_obj = Group.objects.get(name=request.POST.get('role'))
                user_group = User.groups.through.objects.get(user=user)
                user_group.group = group_obj
                user_group.save()
            data['form_is_valid'] = True
            data['users_list'] = render_to_string('ajax_template_accounts/users_list.html',{'users' : User.objects.all()})
        else:
            data['form_is_valid'] = False
            data['err_code'] = 'invalid_form'
            data['err_msg'] = form.errors
    context = {
        "form" : form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def user_create(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
    else:
        form = CreateUserForm()
    return save_all(request, form,'ajax_template_accounts/user_create.html', True )

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def user_update(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=user)
    else:
        form = CreateUserForm(instance=user)
    return save_all(request, form,'ajax_template_accounts/user_update.html', False )

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def user_delete(request, id):
    data = dict()
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user.delete()
        data['form_is_valid'] = True
        data['users_list'] = render_to_string('ajax_template_accounts/users_list.html',{'users' : User.objects.all()})
    else:
        context = {'user' : user}
        data['html_form'] = render_to_string("ajax_template_accounts/user_delete.html", context, request=request)
    return JsonResponse(data)

def user_activate(request, id):
    data = dict()
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        group_obj = Group.objects.get(name='DataAnalyst')
        user_group = User.groups.through.objects.get(user=user)
        user_group.group = group_obj
        user_group.save()
        data['form_is_valid'] = True
        data['users_list'] = render_to_string('ajax_template_accounts/users_list.html',{'users' : User.objects.all()})
    else:
        context = {'user' : user}
        data['html_form'] = render_to_string("ajax_template_accounts/user_activate.html", context, request=request)
    return JsonResponse(data)

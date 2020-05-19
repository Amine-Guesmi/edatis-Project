from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.all()[0].name in ['admin']:
                return redirect('edatis_dashbord:allUsers')
            else:
                return redirect('edatis_dashbord:dashbord')

        return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif group in ['waiter']:
                return redirect('accounts:error403')
            else:
                return redirect('edatis_dashbord:dashbord')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'DataAnalyst':
            return redirect('edatis_dashbord:dashbord')
        if group == 'admin':
            #ajouter page admin en cours de maintenance
            return redirect('edatis_dashbord:dashbord')
    return wrapper_func

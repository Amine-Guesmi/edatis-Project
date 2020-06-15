from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'accounts'

urlpatterns = [
    path('login', views.loginPage, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logoutPage, name='logout'),
    path('error403', views.error403, name='error403'),
    path('dashbord/users/create', views.user_create, name='user_create'),
    path('dashbord/users/<int:id>/update', views.user_update, name='user_update'),
    path('dashbord/users/<int:id>/delete', views.user_delete, name='user_delete'),
    path('dashbord/users/<int:id>/activate', views.user_activate, name='user_activate'),
    #reset Password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="resetPassword.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="resetPasswordDone.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="resetConfirmPassword.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="resetPasswordComplete.html"), name="password_reset_complete"),
]

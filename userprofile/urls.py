from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('logout/', views.user_logout, name='logout'),
    path('switch/', views.user_switch, name='switch'),
    path('delete/<int:id>/', views.user_delete, name='delete'),
    path('edit/<int:id>/', views.profile_edit, name='edit'),
    path('check-username/', views.check_username, name='check_username'),
    path('check-password1/', views.check_password1, name='check_password1'),
    path('check-password2/', views.check_password2, name='check_password2'),
    path('check-email/', views.check_email, name='check_email'),
    path('user-login-check/', views.user_login_check, name='user_login_check'),
]
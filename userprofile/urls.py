from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('logout/', views.user_logout, name='logout'),
    path('switch/', views.user_switch, name='switch'),
    path('delete/<int:id>/', views.user_delete, name='delete'),
    path('edit/<int:id>/', views.profile_edit, name='edit'),
]
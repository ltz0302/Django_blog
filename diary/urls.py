from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('diary-list/', views.diary_list, name='diary_list'),
    path('diary-detail/<int:id>/', views.diary_detail, name='diary_detail'),
    path('diary-create/', views.diary_create, name='diary_create'),
    path('diary-safe-delete/<int:id>/', views.diary_safe_delete, name='diary_safe_delete'),
    path('diary-update/<int:id>/', views.diary_update, name='diary_update'),
]
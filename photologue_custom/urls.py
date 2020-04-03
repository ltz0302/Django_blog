from django.urls import path
from . import views

app_name = 'photologue_custom'

urlpatterns = [
    path('gallery-create/', views.gallery_create, name='gallery_create'),
    path('gallery-delete/<int:id>/', views.gallery_delete, name='gallery_delete'),
    path('photo-add/', views.photo_add, name='photo_add'),
    path('photo-delete/<int:id>/', views.photo_delete, name='photo_delete'),
]
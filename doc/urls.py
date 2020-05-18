from django.urls import path
from . import views

app_name = 'doc'

urlpatterns = [
    path('folder-list/', views.folder_list, name='folder_list'),
    path('folder-create/', views.folder_create, name='folder_create'),
    path('folder-delete/<int:id>/', views.folder_delete, name='folder_delete'),
    path('doc-list/<int:folder>', views.doc_list, name='doc_list'),
    path('doc-add/', views.doc_add, name='doc_add'),
    path('doc-delete/<int:id>/', views.doc_delete, name='doc_delete'),
]
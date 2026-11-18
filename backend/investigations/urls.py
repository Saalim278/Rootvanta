from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_investigation, name="investigation_create"),
    path("", views.investigation_list, name="investigation_list"),
    path("<int:pk>/", views.investigation_detail, name="investigation_detail"),
    path("<int:pk>/edit/", views.edit_investigation, name="investigation_edit"),
    path("<int:pk>/attempt/create/", views.create_fix_attempt, name="create_fix_attempt"),
    path("<int:pk>/reopen/",views.reopen_investigation,name="reopen_investigation"),
    path("<int:pk>/close/",views.close_investigation,name="close_investigation"),
    
]


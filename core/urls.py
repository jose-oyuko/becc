from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),

    # Project CRUD
    path('dashboard/projects/', views.project_list, name='project_list'),
    path('dashboard/projects/add/', views.project_create, name='project_create'),
    path('dashboard/projects/edit/<int:pk>/', views.project_update, name='project_update'),
    path('dashboard/projects/delete/<int:pk>/', views.project_delete, name='project_delete'),
    # Pillar CRUD
    path('dashboard/pillars/', views.pillar_list, name='pillar_list'),
    path('dashboard/pillars/add/', views.pillar_create, name='pillar_create'),
    path('dashboard/pillars/edit/<int:pk>/', views.pillar_update, name='pillar_update'),
    path('dashboard/pillars/delete/<int:pk>/', views.pillar_delete, name='pillar_delete'),
    # Events CRUD
    path('dashboard/events/', views.event_list, name='event_list'),
    path('dashboard/events/add/', views.event_create, name='event_create'),
    path('dashboard/events/edit/<int:pk>/', views.event_update, name='event_update'),
    path('dashboard/events/delete/<int:pk>/', views.event_delete, name='event_delete'),


]

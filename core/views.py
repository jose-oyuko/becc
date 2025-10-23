from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Event, Partner, VolunteerApplication, Donation, Pillar
from django.db import models
from django.contrib import messages
from .forms import ProjectForm, PillarForm, EventForm
from django.urls import reverse

@login_required
def event_list(request):
    events = Event.objects.all().order_by('-date')
    context = {
        "title": "Events",
        "single_name": "Event",
        "plural_name": "Events",
        "headers": ["Title", "Date", "Location", "Status"],
        "fields": ["title", "date", "location", "is_upcoming"],
        "objects": events,
        "add_url": reverse("event_create"),
        "edit_base_url": reverse("event_update", args=[0]).replace("0/", ""),
        "delete_base_url": reverse("event_delete", args=[0]).replace("0/", ""),
    }
    return render(request, "core/crud_list_base.html", context)

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'core/crud_form_base.html', {
        'title': 'Add Event',
        'form': form,
        'back_url': reverse('event_list'),
    })

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'core/crud_form_base.html', {
        'title': 'Edit Event',
        'form': form,
        'back_url': reverse('event_list'),
    })

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    return render(request, 'core/crud_confirm_delete.html', {
        'object': event,
        'single_name': 'Event',
        'back_url': reverse('event_list'),
    })

@login_required
def pillar_list(request):
    pillars = Pillar.objects.all()
    return render(request, 'core/pillar_list.html', {'pillars': pillars})

@login_required
def pillar_create(request):
    if request.method == 'POST':
        form = PillarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pillar added successfully!")
            return redirect('pillar_list')
    else:
        form = PillarForm()
    return render(request, 'core/pillar_form.html', {'form': form, 'title': 'Add Pillar'})

@login_required
def pillar_update(request, pk):
    pillar = get_object_or_404(Pillar, pk=pk)
    if request.method == 'POST':
        form = PillarForm(request.POST, instance=pillar)
        if form.is_valid():
            form.save()
            messages.success(request, "Pillar updated successfully!")
            return redirect('pillar_list')
    else:
        form = PillarForm(instance=pillar)
    return render(request, 'core/pillar_form.html', {'form': form, 'title': 'Edit Pillar'})

@login_required
def pillar_delete(request, pk):
    pillar = get_object_or_404(Pillar, pk=pk)
    if request.method == 'POST':
        pillar.delete()
        messages.success(request, "Pillar deleted successfully!")
        return redirect('pillar_list')
    return render(request, 'core/pillar_confirm_delete.html', {'pillar': pillar})

@login_required
def project_list(request):
    projects = Project.objects.all().order_by('-start_date')
    return render(request, "core/project_list.html", {"projects": projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully!")
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form, 'title': 'Add Project'})

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/project_form.html', {'form': form, 'title': 'Edit Project'})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('project_list')
    return render(request, 'core/project_confirm_delete.html', {'project': project})

@login_required
def dashboard(request):
    projects_count = Project.objects.count()
    active_projects = Project.objects.filter(status="active").count()
    completed_projects = Project.objects.filter(status="completed").count()
    events_count = Event.objects.count()
    partners_count = Partner.objects.count()
    volunteers_count = VolunteerApplication.objects.count()
    total_donations = Donation.objects.all().aggregate(total=models.Sum('amount'))['total'] or 0

    context = {
        "projects_count": projects_count,
        "active_projects": active_projects,
        "completed_projects": completed_projects,
        "events_count": events_count,
        "partners_count": partners_count,
        "volunteers_count": volunteers_count,
        "total_donations": total_donations,
    }
    return render(request, "core/dashboard.html", context)

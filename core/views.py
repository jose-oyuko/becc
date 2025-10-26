from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Event, Partner, VolunteerApplication, Donation, Pillar, Gallery, ContactMessage
from django.db import models
from django.contrib import messages
from .forms import ProjectForm, PillarForm, EventForm, PartnerForm, GalleryForm
from django.urls import reverse
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render

def pillars_page(request):
    # Later we’ll query from Pillar model
    pillars = Pillar.objects.all()
    return render(request, "public/pillars_page.html", {"pillars": pillars})

def projects_page(request):
    projects = Project.objects.all()
    return render(request, "public/projects_page.html", {"projects": projects})

def gallery_page(request):
    gallery = Gallery.objects.all()
    return render(request, "public/gallery_page.html", {"gallery": gallery})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Optional: Save to DB
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Optional: Send email notification
        send_mail(
            subject=f"New message from {name}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["admin@becc.org"],  # Replace with your email
            fail_silently=True,
        )

        messages.success(request, "Thank you for reaching out! We’ll get back to you soon.")
        return redirect("home")

    # If someone directly opens /contact/
    return redirect("home")


def home(request):
    context = {
        "pillars": Pillar.objects.all(),
        "projects": Project.objects.all()[:6],
        "events": Event.objects.all().order_by('-date')[:6],
        "gallery": Gallery.objects.all()[:8],
        "partners": Partner.objects.all(),
        "current_year": datetime.now().year,
    }
    return render(request, "public/home.html", context)


@login_required
def gallery_list(request):
    galleries = Gallery.objects.all().order_by('-uploaded_at')
    context = {
        "title": "Gallery",
        "single_name": "Photo",
        "plural_name": "Gallery",
        "headers": ["Image", "Title", "Event", "Project", "Uploaded"],
        "fields": ["image", "title", "related_event", "related_project", "uploaded_at"],
        "objects": galleries,
        "add_url": reverse("gallery_create"),
        "edit_base_url": reverse("gallery_update", args=[0]).replace("0/", ""),
        "delete_base_url": reverse("gallery_delete", args=[0]).replace("0/", ""),
    }
    return render(request, "core/crud_list_base.html", context)


@login_required
def gallery_create(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo added successfully!")
            return redirect('gallery_list')
    else:
        form = GalleryForm()
    return render(request, 'core/crud_form_base.html', {
        'title': 'Add Photo',
        'form': form,
        'back_url': reverse('gallery_list'),
    })


@login_required
def gallery_update(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo updated successfully!")
            return redirect('gallery_list')
    else:
        form = GalleryForm(instance=gallery)
    return render(request, 'core/crud_form_base.html', {
        'title': 'Edit Photo',
        'form': form,
        'back_url': reverse('gallery_list'),
    })


@login_required
def gallery_delete(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    if request.method == 'POST':
        gallery.delete()
        messages.success(request, "Photo deleted successfully!")
        return redirect('gallery_list')
    return render(request, 'core/crud_confirm_delete.html', {
        'object': gallery,
        'single_name': 'Photo',
        'back_url': reverse('gallery_list'),
    })



@login_required
def partner_list(request):
    partners = Partner.objects.all()
    context = {
        "title": "Partners",
        "single_name": "Partner",
        "plural_name": "Partners",
        "headers": ["Name", "Type", "Website"],
        "fields": ["name", "partner_type", "website"],
        "objects": partners,
        "add_url": reverse("partner_create"),
        "edit_base_url": reverse("partner_update", args=[0]).replace("0/", ""),
        "delete_base_url": reverse("partner_delete", args=[0]).replace("0/", ""),
    }
    return render(request, "core/crud_list_base.html", context)


@login_required
def partner_create(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Partner added successfully!")
            return redirect('partner_list')
    else:
        form = PartnerForm()
    return render(request, 'core/crud_form_base.html', {
        'title': 'Add Partner',
        'form': form,
        'back_url': reverse('partner_list'),
    })


@login_required
def partner_update(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, "Partner updated successfully!")
            return redirect('partner_list')
    else:
        form = PartnerForm(instance=partner)
    return render(request, 'core/crud_form_base.html', {
        'title': 'Edit Partner',
        'form': form,
        'back_url': reverse('partner_list'),
    })


@login_required
def partner_delete(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    if request.method == 'POST':
        partner.delete()
        messages.success(request, "Partner deleted successfully!")
        return redirect('partner_list')
    return render(request, 'core/crud_confirm_delete.html', {
        'object': partner,
        'single_name': 'Partner',
        'back_url': reverse('partner_list'),
    })


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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Event, Partner, VolunteerApplication, Donation, Pillar, Gallery, ContactMessage
from django.db import models
from django.contrib import messages
from .forms import ProjectForm, PillarForm, EventForm, PartnerForm, GalleryForm, PillarGalleryFormSet
from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render

class CustomLoginView(LoginView):
    template_name = "core/auth/login.html"
    redirect_authenticated_user = True

    # after login, send user to dashboard
    def get_success_url(self):
        return reverse_lazy("dashboard")

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")

def projects(request):
    projects = Project.objects.all().select_related('pillar')

    formatted_projects = [
        {
            "title": p.title,
            "category": p.pillar.title if p.pillar else "Uncategorized",
            "image": p.image.url if p.image else "/static/images/placeholder.jpg",
            "description": p.description,
            "impact": p.impact,  # Already a list!
            "status": p.get_status_display(),
        }
        for p in projects
    ]

    return render(request, "public/projects.html", {
        "projects": formatted_projects
    })


def gallery(request):
    gallery_images = [
        {"src": "images/hero-landscape.jpg", "title": "African Landscape Conservation", "category": "Nature"},
        {"src": "images/community-planting.jpg", "title": "Community Tree Planting", "category": "Community"},
        {"src": "images/soil-seedling.jpg", "title": "Sustainable Agriculture", "category": "Agriculture"},
        {"src": "images/water-conservation.jpg", "title": "Water Conservation Project", "category": "Water"},
        {"src": "images/community-planting.jpg", "title": "Environmental Education", "category": "Education"},
        {"src": "images/water-conservation.jpg", "title": "Spring Protection Initiative", "category": "Water"},
    ]
    return render(request, "public/gallery.html", {"gallery_images": gallery_images})


def contact(request):
    if request.method == "POST":
        # Example: you can integrate email sending or save to DB
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        print(name, email, subject, message)  # debug log
    return render(request, "public/contact.html")


def about(request):
    core_values = [
        {
            "title": "Cooperation",
            "description": "Working together with stakeholders and clients to achieve common environmental goals."
        },
        {
            "title": "Inclusivity",
            "description": "Putting ecosystem interests at heart and ensuring all communities benefit."
        },
        {
            "title": "Holistic Approaches",
            "description": "Taking a broad view to address environmental challenges comprehensively."
        },
        {
            "title": "Circularity & Regeneration",
            "description": "Eliminating wastage through sustainable and regenerative practices."
        },
        {
            "title": "Sustainable Technologies",
            "description": "Implementing solutions that benefit current and future generations."
        },
    ]

    context = {
        "core_values": core_values
    }

    return render(request, "public/about.html", context)

def pillars(request):

    db_pillars = Pillar.objects.all()
    pillars = []

    for i, pillar in enumerate(db_pillars):
        pillars.append({
            "title": pillar.title,
            "description": pillar.short_description or pillar.description,
            "activities": pillar.activities,
            "icon": pillar.icon,
            "gallery_images": pillar.gallery_images.all()[:4], # Limit to 4 images
        })
    return render(request, "public/pillars.html", {"pillars": pillars})


def home(request):
    gradients = [
        "bg-gradient-to-br from-green-400 to-green-700",
        "bg-gradient-to-br from-yellow-400 to-yellow-600",
        "bg-gradient-to-br from-sky-400 to-sky-600",
        "bg-gradient-to-br from-emerald-400 to-green-700",
    ]

    db_pillars = Pillar.objects.all()
    pillars = []

    for i, pillar in enumerate(db_pillars):
        gradient = gradients[i % len(gradients)]
        
        # Fetch related gallery images (Limit to 2 for home page)
        # Using reversed relationship 'gallery_images'
        gallery_images = pillar.gallery_images.all()[:2] 

        pillars.append({
            "title": pillar.title,
            "description": pillar.short_description or pillar.description,
            "activities": pillar.activities[:3],
            "icon": pillar.icon,
            "gradient": gradient,
            "gallery_images": gallery_images,
        })
    projects = Project.objects.all().select_related('pillar')[:3]

    formatted_projects = [
        {
            "title": p.title,
            "category": p.pillar.title if p.pillar else "Uncategorized",
            "image": p.image.url if p.image else "/static/images/placeholder.jpg",
            "description": p.description,
        }
        for p in projects
    ]

    projects = [
        
        {
            "title": "Water Harvesting Systems",
            "description": "Installing rainwater harvesting and spring protection systems in rural communities.",
            "image": "/static/images/water-conservation.jpg",
            "category": "Water & Sanitation",
        },
    ]
    context = {
        "pillars": pillars,
        "projects": formatted_projects,
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
        form = PillarForm(request.POST, request.FILES)
        formset = PillarGalleryFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            pillar = form.save()
            images = formset.save(commit=False)
            for image in images:
                image.related_pillar = pillar
                image.save()
            # Handle deletions if any
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, "Pillar added successfully!")
            return redirect('pillar_list')
        else:
            print("Form Errors:", form.errors)
            print("Formset Errors:", formset.errors)
    else:
        form = PillarForm()
        formset = PillarGalleryFormSet()
    return render(request, 'core/pillar_form.html', {'form': form, 'formset': formset, 'title': 'Add Pillar'})

@login_required
def pillar_update(request, pk):
    pillar = get_object_or_404(Pillar, pk=pk)
    if request.method == 'POST':
        form = PillarForm(request.POST, request.FILES, instance=pillar)
        formset = PillarGalleryFormSet(request.POST, request.FILES, instance=pillar)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Pillar updated successfully!")
            return redirect('pillar_list')
    else:
        form = PillarForm(instance=pillar)
        formset = PillarGalleryFormSet(instance=pillar)
    return render(request, 'core/pillar_form.html', {'form': form, 'formset': formset, 'title': 'Edit Pillar'})

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

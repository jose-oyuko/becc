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

def projects(request):
    projects = [
        {
            "title": "Community Tree Planting Initiative",
            "category": "Environmental Protection",
            "image": "images/community-planting.jpg",
            "description": "Large-scale tree planting program restoring degraded forests and lands through collaborative community engagement. We work with local communities to plant indigenous tree species, creating sustainable forests for future generations.",
            "impact": ["5,000+ trees planted", "10 communities involved", "50 hectares restored"],
            "status": "Active",
        },
        {
            "title": "Sustainable Organic Farming Program",
            "category": "Agriculture",
            "image": "images/soil-seedling.jpg",
            "description": "Training farmers in organic farming techniques, indigenous seed conservation, and sustainable agricultural practices. This program promotes food security while protecting soil health and biodiversity.",
            "impact": ["200+ farmers trained", "15 organic farms established", "30 seed varieties preserved"],
            "status": "Active",
        },
        {
            "title": "Water Harvesting & Spring Protection",
            "category": "Water & Sanitation",
            "image": "images/water-conservation.jpg",
            "description": "Installing rainwater harvesting systems and protecting natural springs in rural communities. This initiative ensures clean water access while promoting sustainable water resource management.",
            "impact": ["25 springs protected", "100+ households with harvesting systems", "500,000L water capacity"],
            "status": "Active",
        },
        {
            "title": "Solar Energy Distribution",
            "category": "Entrepreneurship",
            "image": "images/soil-seedling.jpg",
            "description": "Producing and distributing solar energy devices to communities, promoting clean energy adoption and reducing reliance on fossil fuels.",
            "impact": ["150 solar units distributed", "50 businesses supported", "200+ households powered"],
            "status": "Active",
        },
        {
            "title": "Waste Management & Recycling",
            "category": "Environmental Protection",
            "image": "images/community-planting.jpg",
            "description": "Community-based waste collection, recycling, and safe disposal programs. Teaching communities about waste reduction and circular economy principles.",
            "impact": ["5 tons waste recycled monthly", "8 communities served", "30 jobs created"],
            "status": "Active",
        },
        {
            "title": "Apiculture Development",
            "category": "Agriculture",
            "image": "images/water-conservation.jpg",
            "description": "Supporting communities in beekeeping for honey production and pollination services, promoting biodiversity and creating sustainable income sources.",
            "impact": ["80 beehives established", "40 beekeepers trained", "500kg honey produced annually"],
            "status": "Active",
        },
    ]
    return render(request, "public/projects.html", {"projects": projects})


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
    pillars = [
        {
            "title": "Environmental Protection, Conservation & Management",
            "description": "Promote environmental conservation through climate action initiatives that promote flora and fauna in healthy soil, water and air by enhancing green and blue economy technologies.",
            "activities": [
                "Collaborative research and development of technologies",
                "Tree planting in marine and terrestrial lands",
                "Commercial nurseries for trees, fruits, and medicinal plants",
                "Collection and preservation of diverse plant germplasm",
                "Waste collection, reduction, recycling, and safe disposal",
                "Solar energy devices production and marketing",
                "Indigenous seed collection and banking",
                "Wildlife clubs and ethnobotany initiatives",
                "Environmental impact assessment and auditing",
            ],
        },
        {
            "title": "Agriculture, Food & Nutrition Security",
            "description": "Promotion of agriculture, food and nutrition security through technical and financial capacity development for sustainable production, distribution and consumption of food and agro-industrial crops.",
            "activities": [
                "Promoting organic farming practices",
                "Documenting experiential learning by farmers",
                "Hydroponics, floriculture, and olericulture",
                "Apiculture and meliponiculture (bee farming)",
                "Sericulture (silk production)",
                "Vermicomposting for soil enrichment",
                "Indigenous crop variety preservation",
                "Sustainable food production training",
            ],
        },
        {
            "title": "Water, Sanitation & Health",
            "description": "Promote water, sanitation and health advancing technologies by engaging and working with communities for improved socio-economic status for all.",
            "activities": [
                "Water works including supply of equipment and materials",
                "Water harvesting engineering works",
                "Safe water storage technologies (domestic and industrial)",
                "Spring protection initiatives",
                "Rooftop rainfall water harvesting systems",
                "Wetland restoration and rehabilitation",
                "Sustainable irrigation systems",
                "Aquaculture, mariculture, and aquaponics",
            ],
        },
        {
            "title": "Entrepreneurship & Business Development",
            "description": "Promoting entrepreneurship and business development in environmental conservation activities and agribusiness for employment and wealth creation.",
            "activities": [
                "Mobilizing financial resources and investment",
                "Establishment of community demonstration centers",
                "Capacity development through farm visits and exhibitions",
                "Resource mobilization for vulnerable groups",
                "Stakeholder forums for cooperation",
                "Agri and ecotourism ventures",
                "Energy-saving stoves production and marketing",
                "Ecotourism, tours, and travel services",
                "Talent promotion through games, sports, and arts",
                "Nature-based solutions development",
            ],
        },
    ]
    return render(request, "public/pillars.html", {"pillars": pillars})


def home(request):
    icon = """<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4.5V19a1 1 0 0 0 1 1h15M7 14l4-4 4 4 5-5m0 0h-3.207M20 9v3.207"/>
</svg>
"""
    pillars = [
        {
            "icon": "fas fa-tree",
            "title": "Environmental Protection",
            "description": "Climate action initiatives promoting flora and fauna in healthy soil, water, and air through green and blue economy technologies.",
            "gradient": "bg-gradient-to-br from-green-400 to-green-700",
            "activities": ["Tree planting", "Waste management", "Indigenous seed conservation"],
        },
        {
            "icon": "fas fa-seedling",
            "title": "Agriculture & Food Security",
            "description": "Technical and financial capacity development for sustainable production, distribution, and consumption of food and agro-industrial crops.",
            "gradient": "bg-gradient-to-br from-yellow-400 to-yellow-600",
            "activities": ["Organic farming", "Hydroponics", "Apiculture"],
        },
        {
            "icon": "fas fa-water",
            "title": "Water, Sanitation & Health",
            "description": "Advancing technologies by engaging with communities for improved socio-economic status through sustainable water solutions.",
            "gradient": "bg-gradient-to-br from-sky-400 to-sky-600",
            "activities": ["Water harvesting", "Spring protection", "Aquaculture"],
        },
        {
            "icon": "fas fa-chart-line",
            "title": "Entrepreneurship & Business",
            "description": "Promoting business development in environmental conservation and agribusiness for employment and wealth creation.",
            "gradient": "bg-gradient-to-br from-emerald-400 to-green-700",
            "activities": ["Ecotourism", "Community centers", "Resource mobilization"],
        },
    ]
    projects = [
        {
            "title": "Community Tree Planting",
            "description": "Restoration of degraded forests and lands through collaborative community tree planting initiatives.",
            "image": "/static/images/community-planting.jpg",
            "category": "Environmental Protection",
        },
        {
            "title": "Sustainable Agriculture",
            "description": "Promoting organic farming and indigenous seed conservation for food security.",
            "image": "/static/images/soil-seedling.jpg",
            "category": "Agriculture",
        },
        {
            "title": "Water Harvesting Systems",
            "description": "Installing rainwater harvesting and spring protection systems in rural communities.",
            "image": "/static/images/water-conservation.jpg",
            "category": "Water & Sanitation",
        },
    ]
    context = {
        "pillars": pillars,
        "projects": projects,
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

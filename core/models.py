from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/gallery/')
    related_event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True)
    related_project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True)
    related_pillar = models.ForeignKey('Pillar', on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class OrganizationInfo(models.Model):
    name = models.CharField(max_length=255)
    vision = models.TextField()
    mission = models.TextField()
    goal = models.TextField()
    motto = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    about = models.TextField()
    logo = models.ImageField(upload_to='media/logos/', blank=True)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField()
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    x = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    youtube = models.URLField(blank=True)


    def __str__(self):
        return self.name
    
class Pillar(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.TextField(
        blank=True,
        help_text="Optional shorter version for home page"
    )
    icon = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='media/pillars/', blank=True)
    activities = JSONField(
        default=list,
        help_text="A list of activities displayed on detailed page & home page"
    )

    def __str__(self):
        return self.title

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('upcoming', 'Upcoming'),
    ]

    title = models.CharField(max_length=255)
    pillar = models.ForeignKey(Pillar, on_delete=models.CASCADE, related_name='projects')
    short_description = models.TextField(blank=True, help_text="A short summary for list views.")
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/projects/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    impact = ArrayField(
        base_field=models.TextField(),
        blank=True,
        default=list,
        help_text="Enter a list of impact points. Each entry can be long or short."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ProjectMedia(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField(upload_to='media/project_media/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Media for {self.project.title}"
    
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255, blank=True)
    registration_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='media/events/', blank=True)
    is_upcoming = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Partner(models.Model):
    TYPE_CHOICES = [
        ('ngo', 'NGO'),
        ('government', 'Government'),
        ('academic', 'Academic Institution'),
        ('private', 'Private Sector'),
        ('community', 'Community Group'),
    ]

    name = models.CharField(max_length=255)
    partner_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='media/partners/', blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='media/team/', blank=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='media/blog/', blank=True)
    category = models.CharField(max_length=100, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class VolunteerApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Donation(models.Model):
    donor_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=[
        ('mpesa', 'M-Pesa'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
    ])
    transaction_id = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount}"


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=255)
    hero_image = models.ImageField(upload_to='media/hero/', blank=True)
    about_intro = models.TextField(blank=True)
    footer_text = models.TextField(blank=True)

    def __str__(self):
        return self.site_name



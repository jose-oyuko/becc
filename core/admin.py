from django.contrib import admin
from .models import (
    OrganizationInfo,
    Pillar,
    Project,
    ProjectMedia,
    Event,
    Partner,
    TeamMember,
    BlogPost,
    VolunteerApplication,
    Donation,
    HeroImage
)

# Optional: Inline for project media
class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 1

class HeroImageInline(admin.TabularInline):
    model = HeroImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'pillar', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'pillar')
    search_fields = ('title', 'description', 'location')
    inlines = [ProjectMediaInline]
    ordering = ('-start_date',)


@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_upcoming')
    list_filter = ('is_upcoming',)
    search_fields = ('title', 'location')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'website')
    list_filter = ('partner_type',)
    search_fields = ('name',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'contact_email')
    search_fields = ('name', 'position')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published', 'created_at')
    list_filter = ('published', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(VolunteerApplication)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'approved', 'submitted_at')
    list_filter = ('approved',)
    search_fields = ('name', 'email')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'method', 'date')
    list_filter = ('method',)
    search_fields = ('donor_name', 'transaction_id')


@admin.register(OrganizationInfo)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone')
    inlines = [HeroImageInline]

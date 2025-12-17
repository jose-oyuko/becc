from django import forms
from .models import Project, Pillar, Event, Partner, Gallery, OrganizationInfo, HeroImage
import json

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'image', 'related_event', 'related_project']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 3}),
            'related_event': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'related_project': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'partner_type', 'description', 'website', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'partner_type': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }


class ProjectForm(forms.ModelForm):
    # Hidden field that will store JSON impact list
    impact_json = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.impact:
            # Impact is already a list (ArrayField), so just dump it
            self.fields['impact_json'].initial = json.dumps(self.instance.impact)

    class Meta:
        model = Project
        fields = [
            'title', 'pillar', 'short_description', 'description', 'location',
            'start_date', 'end_date', 'status', 'image', 'impact_json'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'pillar': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'short_description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
            'status': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }

    def clean(self):
        cleaned = super().clean()
        
        # Parse JSON stored in hidden field
        impact_raw = cleaned.get("impact_json", "[]")
        
        try:
            cleaned["impact"] = json.loads(impact_raw)
        except json.JSONDecodeError:
            self.add_error("impact_json", "Invalid impact format.")
            cleaned["impact"] = []
        
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Manually assign impact from cleaned_data
        if "impact" in self.cleaned_data:
            instance.impact = self.cleaned_data["impact"]
        
        if commit:
            instance.save()
        return instance


class PillarForm(forms.ModelForm):
    # Hidden field that will store JSON activities list
    activities_json = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.activities:
            self.fields['activities_json'].initial = json.dumps(self.instance.activities)

    class Meta:
        model = Pillar
        fields = [
            "short_description",
            "title",
            "description",
            # "image", Removed as per request
            "activities_json",    # NOT the original JSONField
        ]

        widgets = {
            "short_description": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded-lg",
                "rows": 3,
            }),
            "title": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded-lg",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded-lg",
                "rows": 4,
            }),
            # "image": forms.ClearableFileInput(attrs={
            #     "class": "w-full",
            # }),
        }

    def clean(self):
        cleaned = super().clean()
        
        # Parse JSON stored in hidden field
        activities_raw = cleaned.get("activities_json", "[]")
        
        try:
            cleaned["activities"] = json.loads(activities_raw)
        except json.JSONDecodeError:
            self.add_error("activities_json", "Invalid activities format.")
            cleaned["activities"] = []
        
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Manually assign activities from cleaned_data since it's not in Meta.fields
        if "activities" in self.cleaned_data:
            instance.activities = self.cleaned_data["activities"]
        
        if commit:
            instance.save()
        return instance


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'is_upcoming', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
            'location': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'is_upcoming': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }

from django.forms import inlineformset_factory
PillarGalleryFormSet = inlineformset_factory(
    Pillar, Gallery, 
    fields=['image', 'title', 'description'],
    widgets = {
        'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Image Title'}),
        'description': forms.Textarea(attrs={'class': 'hidden', 'rows': 2, 'placeholder': 'Short description'}), # Hidden because we handle it via JS ui? Or expose it? User said "small description attached". Let's expose it in JS UI, store in hidden or normal input.
        'image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
    },
    extra=1,
    can_delete=True
)

ProjectGalleryFormSet = inlineformset_factory(
    Project, Gallery, 
    fields=['image', 'title', 'description'],
    widgets = {
        'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Image Title'}),
        'description': forms.Textarea(attrs={'class': 'hidden', 'rows': 2, 'placeholder': 'Short description'}),
        'image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
    },
    extra=1,
    can_delete=True
)


class OrganizationInfoForm(forms.ModelForm):
    # Hidden field for JSON handling
    core_values_json = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Load existing JSON
            self.fields['core_values_json'].initial = json.dumps(self.instance.core_values)

    class Meta:
        model = OrganizationInfo
        fields = [
            'name', 'logo', 'contact_email', 'phone', 'address',
            'facebook', 'instagram', 'x', 'tiktok', 'youtube',
            'vision', 'mission', 'goal', 'motto', 'slogan', 'about', 'about_background',
            'hero_title', 'hero_subtitle', 
            'paybill_no', 'account_no',
            'footer_text', 'meta_description', 'meta_keywords',
            'core_values_json'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'contact_email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'address': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 3}),
            
            'facebook': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'https://facebook.com/...'}),
            'instagram': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'x': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'tiktok': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'youtube': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-lg'}),

            'vision': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 2}),
            'mission': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 2}),
            'goal': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 2}),
            'motto': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'slogan': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'about': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 4, 'placeholder': 'Short intro about the org'}),
            'about_background': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 6}),

            'hero_title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'hero_subtitle': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 2}),

            'paybill_no': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'account_no': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),

            'footer_text': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 2}),
            'meta_description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 2}),
            'meta_keywords': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }

    def clean(self):
        cleaned = super().clean()
        core_values_raw = cleaned.get("core_values_json", "[]")
        try:
            cleaned["core_values"] = json.loads(core_values_raw)
        except json.JSONDecodeError:
            self.add_error("core_values_json", "Invalid JSON format.")
            cleaned["core_values"] = []
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        if "core_values" in self.cleaned_data:
            instance.core_values = self.cleaned_data["core_values"]
        if commit:
            instance.save()
        return instance

HeroImageFormSet = inlineformset_factory(
    OrganizationInfo, HeroImage,
    fields=['image', 'caption', 'order'],
    widgets={
        'image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        'caption': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Caption'}),
        'order': forms.NumberInput(attrs={'class': 'w-20 p-2 border rounded-lg', 'placeholder': 'Order'}),
    },
    extra=1,
    can_delete=True
)
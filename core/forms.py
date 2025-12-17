from django import forms
from .models import Project, Pillar, Event, Partner, Gallery
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
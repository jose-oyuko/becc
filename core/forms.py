from django import forms
from .models import Project, Pillar, Event, Partner

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
    class Meta:
        model = Project
        fields = ['title', 'pillar', 'description', 'location', 'start_date', 'end_date', 'status', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'pillar': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
            'status': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }

class PillarForm(forms.ModelForm):
    class Meta:
        model = Pillar
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 3}),
        }

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
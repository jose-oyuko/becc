import os
import django
import json
from django.conf import settings

# Setup Django standalone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beccsite.settings')
django.setup()

from core.forms import PillarForm
from core.models import Pillar

#  Create a dummy pillar in memory (not saving to avoid DB pollution if possible, but form needs instance)
# Actually, form needs instance.activities.
class MockPillar:
    def __init__(self):
        self.pk = 1
        self.activities = ["Activity A", "Activity B"]
        self.image = None # Not testing image url generation here, just logic

# Instantiate form
mock_instance = MockPillar()
form = PillarForm(instance=mock_instance)

# Check initial data
print(f"Activities JSON Initial: {form.fields['activities_json'].initial}")

# Expected output: '["Activity A", "Activity B"]'

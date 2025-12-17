from .models import OrganizationInfo

def organization_info(request):
    """
    Makes organization info available in all templates.
    """
    return {
        'org_info': OrganizationInfo.objects.first()
    }

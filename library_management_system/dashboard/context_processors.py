from catalog.models import Review


def dashboard_notifications(request):
    if not request.user.is_authenticated or not request.user.is_admin():
        return {}
    return {
        'resenas_pendientes': Review.objects.filter(aprobada=False).count(),
    }
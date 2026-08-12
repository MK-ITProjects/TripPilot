from .models import Destination


def footer_destinations(request):
    top = list(Destination.objects.order_by('-previous_visitor_count')[:5])
    top_ids = [d.id for d in top]
    trending = list(Destination.objects.exclude(id__in=top_ids).order_by('-created_at')[:5])
    return {
        'footer_top_destinations': top,
        'footer_trending_destinations': trending,
    }

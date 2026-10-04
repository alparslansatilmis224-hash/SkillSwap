from .models import Category
from django.db.models import Count


def categories_processor(request):
    """
    Tüm şablonlara kategorileri ve bu kategorilerdeki aktif ilan sayılarını sağlar.
    """
    try:
        categories = Category.objects.annotate(listing_count=Count('listings')).order_by('name')
        return {'all_categories': categories}
    except Exception:
        return {'all_categories': []}

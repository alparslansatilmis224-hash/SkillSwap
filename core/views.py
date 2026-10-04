from django.views.generic import TemplateView
from listings.models import SkillListing, Category
from swaps.models import SwapRequest
from users.models import CustomUser


class HomeView(TemplateView):
    """
    SkillSwap Ana Sayfa Görünümü.
    Hero section, son eklenen 6 ilan ve platform istatistiklerini sunar.
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # En son eklenen 6 yetenek ilanı
        latest_listings = SkillListing.objects.select_related(
            'provider', 'category'
        ).order_by('-created_at')[:6]

        # Popüler kategoriler
        categories = Category.objects.all()[:6]

        # Platform İstatistikleri
        total_listings = SkillListing.objects.count()
        total_users = CustomUser.objects.count()
        completed_swaps = SwapRequest.objects.filter(status='accepted').count()

        context.update({
            'latest_listings': latest_listings,
            'featured_categories': categories,
            'stats': {
                'total_listings': total_listings if total_listings > 0 else "500+",
                'total_users': total_users if total_users > 0 else "1,200+",
                'completed_swaps': completed_swaps if completed_swaps > 0 else "350+",
            }
        })
        return context

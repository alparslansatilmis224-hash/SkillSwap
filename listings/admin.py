from django.contrib import admin
from .models import Category, SkillListing


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category modeli için admin yapılandırması.
    """
    list_display = ('name', 'slug', 'listing_count_display')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def listing_count_display(self, obj):
        return obj.listings.count()
    listing_count_display.short_description = "İlan Sayısı"


@admin.register(SkillListing)
class SkillListingAdmin(admin.ModelAdmin):
    """
    SkillListing modeli için admin yapılandırması.
    """
    list_display = ('title', 'category', 'provider', 'difficulty_level', 'swap_requests_count', 'created_at')
    list_filter = ('category', 'difficulty_level', 'created_at')
    search_fields = ('title', 'description', 'provider__username', 'provider__first_name', 'provider__last_name', 'provider__email')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def swap_requests_count(self, obj):
        return obj.swap_requests.count()
    swap_requests_count.short_description = "Teklif Sayısı"

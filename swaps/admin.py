from django.contrib import admin
from .models import SwapRequest


@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    """
    SwapRequest modeli için admin yapılandırması.
    """
    list_display = ('id', 'listing_title', 'provider_name', 'requester_name', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'listing__category')
    search_fields = (
        'message',
        'requester__username',
        'requester__email',
        'listing__title',
        'listing__provider__username'
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def listing_title(self, obj):
        return obj.listing.title
    listing_title.short_description = "İlan Başlığı"

    def provider_name(self, obj):
        return obj.listing.provider.username
    provider_name.short_description = "İlan Sahibi"

    def requester_name(self, obj):
        return obj.requester.username
    requester_name.short_description = "Teklif Eden"

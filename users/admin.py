from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    CustomUser modeli için özelleştirilmiş Admin paneli yapılandırması.
    """
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'location', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'location')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'location', 'bio')
    ordering = ('-date_joined',)

    # UserAdmin fieldsets'lerine özel alanları (bio, avatar, location) dahil ediyoruz
    fieldsets = UserAdmin.fieldsets + (
        ('SkillSwap Profil Bilgileri', {
            'fields': ('bio', 'avatar', 'location'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('SkillSwap Profil Bilgileri', {
            'fields': ('email', 'first_name', 'last_name', 'bio', 'avatar', 'location'),
        }),
    )

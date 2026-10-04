from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomLoginForm, UserProfileUpdateForm


class RegisterView(CreateView):
    """
    Yeni kullanıcı kaydı oluşturma ve otomatik oturum açma görünümü.
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"SkillSwap platformuna hoş geldiniz, {user.username}! Profiliniz başarıyla oluşturuldu.")
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    """
    Kullanıcı giriş görünümü.
    """
    authentication_form = CustomLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Tekrar hoş geldiniz, {form.get_user().username}!")
        return super().form_valid(form)


class CustomLogoutView(View):
    """
    Kullanıcı güvenli çıkış görünümü (GET ve POST destekler).
    """
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            messages.info(request, f"Görüşmek üzere {username}, başarıyla çıkış yaptınız.")
        return redirect('home')


class UserProfileView(LoginRequiredMixin, TemplateView):
    """
    Kullanıcı Profil ve Yönetim Paneli (Dashboard).
    Kullanıcının bilgilerini, verdiği yetenek ilanlarını ve gelen/giden takas tekliflerini listeler.
    """
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Kullanıcının verdiği ilanlar
        my_listings = user.skill_listings.select_related('category').prefetch_related('swap_requests').all()

        # Kullanıcıya gelen takas teklifleri (Kullanıcının ilanlarına yapılan teklifler)
        # listings__provider = user
        from swaps.models import SwapRequest
        received_swaps = SwapRequest.objects.filter(
            listing__provider=user
        ).select_related('listing', 'requester').order_by('-created_at')

        # Kullanıcının başkalarına gönderdiği takas teklifleri
        sent_swaps = user.sent_swap_requests.select_related('listing', 'listing__provider').order_by('-created_at')

        context.update({
            'my_listings': my_listings,
            'received_swaps': received_swaps,
            'sent_swaps': sent_swaps,
            'stats': {
                'listings_count': my_listings.count(),
                'received_count': received_swaps.count(),
                'sent_count': sent_swaps.count(),
                'accepted_count': received_swaps.filter(status='accepted').count() + sent_swaps.filter(status='accepted').count(),
                'pending_received_count': received_swaps.filter(status='pending').count(),
            }
        })
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Kullanıcının kendi profil bilgilerini ve avatarını güncelleme görünümü.
    """
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profil bilgileriniz başarıyla güncellendi.")
        return super().form_valid(form)

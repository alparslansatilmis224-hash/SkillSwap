from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q

from .models import SkillListing, Category
from .forms import SkillListingForm


class SkillListingListView(ListView):
    """
    Tüm yetenek ilanlarını listeleme, kategoriye göre filtreleme ve arama görünümü.
    """
    model = SkillListing
    template_name = 'listings/listing_list.html'
    context_object_name = 'listings'
    paginate_by = 9

    def get_queryset(self):
        queryset = SkillListing.objects.select_related('category', 'provider').all()

        # Arama sorgusu (q)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(provider__username__icontains=query)
            )

        # Kategori filtresi
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Zorluk derecesi filtresi
        difficulty = self.request.GET.get('difficulty')
        if difficulty in ['beginner', 'intermediate', 'advanced']:
            queryset = queryset.filter(difficulty_level=difficulty)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        context['current_difficulty'] = self.request.GET.get('difficulty', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class SkillListingDetailView(DetailView):
    """
    Tek bir yetenek ilanının detaylarını ve takas teklifi formunu gösteren görünüm.
    """
    model = SkillListing
    template_name = 'listings/listing_detail.html'
    context_object_name = 'listing'

    def get_queryset(self):
        return SkillListing.objects.select_related('category', 'provider')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listing = self.object
        user = self.request.user

        # Aynı kategorideki diğer ilgili ilanlar (kendisi hariç)
        context['related_listings'] = SkillListing.objects.filter(
            category=listing.category
        ).exclude(pk=listing.pk).select_related('provider', 'category')[:3]

        # Takas formu ve mevcut teklif kontrolü
        if user.is_authenticated:
            from swaps.forms import SwapRequestForm
            from swaps.models import SwapRequest
            context['swap_form'] = SwapRequestForm()
            context['existing_swap'] = SwapRequest.objects.filter(
                listing=listing,
                requester=user
            ).first()
        else:
            context['swap_form'] = None
            context['existing_swap'] = None

        return context


class SkillListingCreateView(LoginRequiredMixin, CreateView):
    """
    Yeni yetenek ilanı oluşturma görünümü.
    """
    model = SkillListing
    form_class = SkillListingForm
    template_name = 'listings/listing_form.html'

    def form_valid(self, form):
        form.instance.provider = self.request.user
        messages.success(self.request, "Tebrikler! Yetenek ilanınız başarıyla yayına alındı.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Yeni Yetenek İlanı Oluştur"
        context['button_text'] = "İlanı Yayınla"
        return context


class SkillListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Yetenek ilanını düzenleme görünümü (Yalnızca ilan sahibi erişebilir).
    """
    model = SkillListing
    form_class = SkillListingForm
    template_name = 'listings/listing_form.html'

    def test_func(self):
        listing = self.get_object()
        return listing.provider == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "İlanınız başarıyla güncellendi.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "İlanı Düzenle"
        context['button_text'] = "Değişiklikleri Kaydet"
        return context


class SkillListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Yetenek ilanını silme görünümü (Yalnızca ilan sahibi silebilir).
    """
    model = SkillListing
    template_name = 'listings/listing_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        listing = self.get_object()
        return listing.provider == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Yetenek ilanı başarıyla silindi.")
        return super().delete(request, *args, **kwargs)

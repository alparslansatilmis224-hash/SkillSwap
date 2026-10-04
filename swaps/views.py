from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

from listings.models import SkillListing
from .models import SwapRequest
from .forms import SwapRequestForm


class CreateSwapRequestView(LoginRequiredMixin, View):
    """
    Kullanıcının bir ilana takas teklifi oluşturmasını sağlayan görünüm.
    """
    def post(self, request, listing_id):
        listing = get_object_or_404(SkillListing, pk=listing_id)

        # Kendi ilanına teklif yapma engeli
        if listing.provider == request.user:
            messages.error(request, "Kendi ilanınıza takas teklifinde bulunamazsınız.")
            return redirect('listing_detail', pk=listing.pk)

        # Daha önce teklif yapılmış mı kontrolü
        existing_request = SwapRequest.objects.filter(listing=listing, requester=request.user).first()
        if existing_request and existing_request.status == SwapRequest.STATUS_PENDING:
            messages.warning(request, "Bu ilan için zaten bekleyen bir takas teklifiniz bulunuyor.")
            return redirect('listing_detail', pk=listing.pk)

        form = SwapRequestForm(request.POST)
        if form.is_valid():
            if existing_request:
                # Daha önce reddedilmişse veya yeni mesajla güncelliyorsa
                existing_request.message = form.cleaned_data['message']
                existing_request.status = SwapRequest.STATUS_PENDING
                existing_request.save()
            else:
                swap = form.save(commit=False)
                swap.listing = listing
                swap.requester = request.user
                swap.status = SwapRequest.STATUS_PENDING
                swap.save()

            messages.success(request, f"'{listing.title}' ilanı için takas teklifiniz başarıyla iletildi!")
        else:
            messages.error(request, "Teklif gönderilirken bir hata oluştu. Lütfen mesaj alanını kontrol edin.")

        return redirect('listing_detail', pk=listing.pk)


class UpdateSwapRequestStatusView(LoginRequiredMixin, View):
    """
    İlan sahibinin gelen takas teklifini kabul veya red etmesini sağlayan görünüm.
    """
    def post(self, request, pk, action):
        return self._process_status(request, pk, action)

    def get(self, request, pk, action):
        return self._process_status(request, pk, action)

    def _process_status(self, request, pk, action):
        swap = get_object_or_404(SwapRequest, pk=pk)

        # Yalnızca ilan sahibi teklif durumunu değiştirebilir
        if swap.listing.provider != request.user:
            messages.error(request, "Bu işlem için yetkiniz bulunmamaktadır.")
            return redirect('profile')

        if action == 'accept':
            swap.status = SwapRequest.STATUS_ACCEPTED
            swap.save()
            messages.success(
                request,
                f"Tebrikler! {swap.requester.get_full_name() or swap.requester.username} kullanıcısının takas teklifini kabul ettiniz. "
                f"Kullanıcı e-postası: {swap.requester.email}"
            )
        elif action == 'reject':
            swap.status = SwapRequest.STATUS_REJECTED
            swap.save()
            messages.info(request, f"{swap.requester.username} kullanıcısının teklifi reddedildi.")
        else:
            messages.error(request, "Geçersiz işlem parametresi.")

        return redirect('profile')

from django.db import models
from django.conf import settings


class SwapRequest(models.Model):
    """
    Kullanıcıların bir yetenek ilanına gönderdikleri Takas Teklifi Modeli.
    """
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Beklemede (Pending)'),
        (STATUS_ACCEPTED, 'Kabul Edildi (Accepted)'),
        (STATUS_REJECTED, 'Reddedildi (Rejected)'),
    ]

    listing = models.ForeignKey(
        'listings.SkillListing',
        on_delete=models.CASCADE,
        related_name='swap_requests',
        verbose_name="İlgili Yetenek İlanı"
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_swap_requests',
        verbose_name="Teklifi Yapan Kullanıcı"
    )
    message = models.TextField(
        verbose_name="Takas Teklifi Mesajı",
        help_text="Bu yeteneği neden öğrenmek istediğinizi ve karşılığında hangi beceriyi sunabileceğinizi açıklayın."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Teklif Durumu"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Teklif Tarihi"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Son Güncellenme Tarihi"
    )

    class Meta:
        verbose_name = "Takas Teklifi"
        verbose_name_plural = "Takas Teklifleri"
        ordering = ['-created_at']
        unique_together = ('listing', 'requester')

    def __str__(self):
        return f"{self.requester.username} -> {self.listing.title} ({self.get_status_display()})"

    @property
    def status_badge_classes(self):
        """Tailwind badge color mapping for status."""
        colors = {
            self.STATUS_PENDING: 'bg-amber-50 text-amber-700 ring-1 ring-amber-600/20',
            self.STATUS_ACCEPTED: 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20',
            self.STATUS_REJECTED: 'bg-rose-50 text-rose-700 ring-1 ring-rose-600/20',
        }
        return colors.get(self.status, 'bg-gray-50 text-gray-700 ring-1 ring-gray-600/20')

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """
    Yetenek Kategorisi Modeli (Örn: Yazılım, Dil Öğrenimi, Müzik, vb.)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Kategori Açıklaması")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c'))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"{reverse('listing_list')}?category={self.slug}"


class SkillListing(models.Model):
    """
    Kullanıcıların başkalarına öğretebilecekleri becerileri sundukları Yetenek İlanı Modeli.
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Başlangıç (Beginner)'),
        ('intermediate', 'Orta Seviye (Intermediate)'),
        ('advanced', 'İleri Seviye (Advanced)'),
    ]

    title = models.CharField(max_length=200, verbose_name="İlan Başlığı")
    description = models.TextField(verbose_name="Yeteneğin Açıklaması ve Öğretebilecekleriniz")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name="Kategori"
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skill_listings',
        verbose_name="Eğitmen / İlan Sahibi"
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner',
        verbose_name="Zorluk Seviyesi"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Yetenek İlanı"
        verbose_name_plural = "Yetenek İlanları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.provider.username}"

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'pk': self.pk})

    @property
    def difficulty_badge_classes(self):
        """Tailwind badge color mapping for difficulty level."""
        colors = {
            'beginner': 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20',
            'intermediate': 'bg-blue-50 text-blue-700 ring-1 ring-blue-600/20',
            'advanced': 'bg-purple-50 text-purple-700 ring-1 ring-purple-600/20',
        }
        return colors.get(self.difficulty_level, 'bg-gray-50 text-gray-700 ring-1 ring-gray-600/20')

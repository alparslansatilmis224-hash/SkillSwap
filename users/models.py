from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    SkillSwap Özel Kullanıcı Modeli.
    AbstractUser sınıfını genişleterek bio, avatar ve location alanları ekler.
    """
    bio = models.TextField(
        blank=True,
        verbose_name="Hakkında / Biyografi",
        help_text="Kendinizden, ilgi alanlarınızdan ve öğretmek/öğrenmek istediğiniz konulardan bahsedin."
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Profil Fotoğrafı"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Konum / Şehir",
        help_text="Örn: İstanbul, Ankara veya Online"
    )

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"
        ordering = ['-date_joined']

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username

    @property
    def avatar_url(self):
        """Kullanıcının avatarı varsa URL'sini, yoksa UI-Avatars servisinden dinamik görsel URL'si döndürür."""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        name = self.get_full_name() or self.username
        return f"https://ui-avatars.com/api/?name={name}&background=4f46e5&color=fff&size=128&bold=true"

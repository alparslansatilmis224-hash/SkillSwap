"""
Core app models.
Can hold sitewide models or abstract base timestamp models if needed.
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    Tüm modeller için ortak zaman damgası sağlayan soyut temel model.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        abstract = True

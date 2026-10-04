from django import forms
from .models import SwapRequest


TAILWIND_TEXTAREA = (
    "w-full px-4 py-3 text-gray-900 bg-white border border-gray-300 rounded-xl "
    "focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out "
    "placeholder-gray-400 text-sm shadow-sm resize-y"
)


class SwapRequestForm(forms.ModelForm):
    """
    Takas Teklifi Gönderme Formu.
    """
    class Meta:
        model = SwapRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 4,
                'placeholder': 'Merhaba! Bu yeteneği öğrenmek çok isterim. Karşılığında sana orta seviye Web Tasarımı / İngilizce Konuşma Pratiği öğretebilirim. Haftada 2 saat uygun olur mu?'
            })
        }
        labels = {
            'message': 'Teklif Mesajınız ve Sunabileceğiniz Yetenek'
        }

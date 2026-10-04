from django import forms
from .models import SkillListing


TAILWIND_INPUT = (
    "w-full px-4 py-2.5 text-gray-900 bg-white border border-gray-300 rounded-xl "
    "focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out "
    "placeholder-gray-400 text-sm shadow-sm"
)

TAILWIND_SELECT = (
    "w-full px-4 py-2.5 text-gray-900 bg-white border border-gray-300 rounded-xl "
    "focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out "
    "text-sm shadow-sm"
)

TAILWIND_TEXTAREA = (
    "w-full px-4 py-2.5 text-gray-900 bg-white border border-gray-300 rounded-xl "
    "focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out "
    "placeholder-gray-400 text-sm shadow-sm resize-y"
)


class SkillListingForm(forms.ModelForm):
    """
    Yetenek İlanı Oluşturma ve Düzenleme Formu.
    """
    class Meta:
        model = SkillListing
        fields = ['title', 'category', 'difficulty_level', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Örn: Sıfırdan İleri Seviyeye Python & Django Geliştirme'
            }),
            'category': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'difficulty_level': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'description': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 6,
                'placeholder': 'Bu yetenekte neleri kapsayacaksınız? Karşılığında ne tür bir beceri öğrenmek istersiniz?'
            }),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


TAILWIND_INPUT_CLASSES = (
    "w-full px-4 py-2.5 text-gray-900 bg-white border border-gray-300 rounded-xl "
    "focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out "
    "placeholder-gray-400 text-sm shadow-sm"
)

TAILWIND_TEXTAREA_CLASSES = (
    "w-full px-4 py-2.5 text-gray-900 bg-white border border-gray-300 rounded-xl "
    "focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out "
    "placeholder-gray-400 text-sm shadow-sm resize-y"
)

TAILWIND_FILE_CLASSES = (
    "w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl "
    "file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 "
    "hover:file:bg-indigo-100 transition duration-150 cursor-pointer"
)


class CustomUserCreationForm(UserCreationForm):
    """
    Kullanıcı Kayıt (Register) Formu.
    """
    email = forms.EmailField(
        required=True,
        label="E-posta Adresi",
        widget=forms.EmailInput(attrs={
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': 'ornek@email.com'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'location', 'bio', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': TAILWIND_TEXTAREA_CLASSES, 'rows': 3})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': TAILWIND_FILE_CLASSES})
            else:
                field.widget.attrs.update({'class': TAILWIND_INPUT_CLASSES})


class UserProfileUpdateForm(forms.ModelForm):
    """
    Kullanıcı Profil Güncelleme Formu.
    """
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'location', 'bio', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': TAILWIND_TEXTAREA_CLASSES, 'rows': 4})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': TAILWIND_FILE_CLASSES})
            else:
                field.widget.attrs.update({'class': TAILWIND_INPUT_CLASSES})


class CustomLoginForm(AuthenticationForm):
    """
    Kullanıcı Giriş (Login) Formu.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': 'Kullanıcı adınız'
        })
        self.fields['password'].widget.attrs.update({
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': '••••••••'
        })

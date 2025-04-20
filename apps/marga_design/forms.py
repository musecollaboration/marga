from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from apps.marga_design.models import BlogPost
from django import forms
from .models import Application


class AuthorForm(forms.ModelForm):
    """Форма для обратной связи"""

    recaptcha = ReCaptchaField()

    class Meta:
        model = Application
        fields = ["name", "email", "phone", "message", 'recaptcha']

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Иванов Иван Иванович"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "ivanov@mail.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+79991234567"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Введите сообщение"}),
        }

        labels = {
            "name": "ФИО",
            "email": "Email",
            "phone": "Телефон",
            "message": "Сообщение",
        }

        help_texts = {
            "phone": "Введите номер в международном формате",
        }

class CreateBlogPostForm(forms.ModelForm):
    """Форма для создания нового блога"""

    class Meta:
        model = BlogPost
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

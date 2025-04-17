from django.forms import ModelForm, CharField

from apps.marga_design.models import Application
from django import forms
from .models import Application


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "email", "phone", "message"]

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

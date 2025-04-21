from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации на сайте
    """

    recaptcha = ReCaptchaField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'recaptcha']

    def __init__(self, *args, **kwargs):
        """
        Обновление атрибутов полей формы регистрации
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Логин'

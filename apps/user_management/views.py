from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import UpdateView, DetailView

from apps.marga_design.forms import AuthorForm
from apps.marga_design.models import Application
from apps.user_management.forms import UserLoginForm
from apps.user_management.models import Profile

from django.views.generic import ListView


class ProfilePage(ListView):
    model = Application
    template_name = "user_management/profile.html"
    context_object_name = "applications"
    paginate_by = 3  # Количество заявок на странице

    def get_queryset(self):
        return Application.objects.select_related("user__profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile  # Профиль текущего пользователя
        return context  # Не переопределяем `applications`, чтобы пагинация работала


class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование заявки"""
    model = Application
    template_name = "user_management/application_edit.html"
    form_class = AuthorForm

    def get_success_url(self):
        return reverse("user_management:user", kwargs={"slug": self.object.user.profile.slug})

    def form_valid(self, form):
        print(form.cleaned_data)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Application.objects.select_related("user__profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.user:
            context["profile"] = self.object.user.profile
        return context

        # def form_invalid(self, form):

    #     print("Форма не прошла валидацию")
    #     print(form.errors)  # Вывод ошибок валидации
    #     return super().form_invalid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if self.request.user.is_staff:  # Проверяем, сотрудник ли это
            del form.fields["message"]  # Удаляем поле для клиентов
            del form.fields['recaptcha']
        return form


class CustomLoginView(LoginView):
    form_class = UserLoginForm

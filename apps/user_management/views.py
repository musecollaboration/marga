from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views.generic import UpdateView

from apps.marga_design.forms import AuthorForm
from apps.marga_design.models import Application
from apps.user_management.forms import UserLoginForm

from django.views.generic import ListView


class ProfilePage(PermissionRequiredMixin, ListView):
    model = Application
    template_name = "user_management/profile.html"
    context_object_name = "applications"
    paginate_by = 3  # Количество заявок на странице
    permission_required = "user_management.view_profile"  # Права доступа к странице профиля

    def get_queryset(self):
        return Application.objects.select_related("user__profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile  # Профиль текущего пользователя
        current_page = self.request.GET.get("page", 1)
        self.request.session["current_page"] = current_page  # Сохраняем в сессию
        context["current_page"] = current_page
        return context  # Не переопределяем `applications`, чтобы пагинация работала


class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование заявки"""
    model = Application
    template_name = "user_management/application_edit.html"
    form_class = AuthorForm

    def get_success_url(self):
        page = self.request.session.get("current_page", 1)  # Берем из сессии
        return f"{reverse('user_management:user', kwargs={'slug': self.object.user.profile.slug})}?page={page}"

    def form_valid(self, form):
        # print(form.cleaned_data)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Application.objects.select_related("user__profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Берем `page` либо из GET-запроса, либо из сессии
        current_page = self.request.GET.get("page", self.request.session.get("current_page", 1))  # Берем из GET или сессии
        self.request.session["current_page"] = current_page  # Сохраняем в сессию
        context["current_page"] = current_page
        if self.object.user:
            context["profile"] = self.object.user.profile
        return context

    # def form_invalid(self, form):
    #     print("Форма не прошла валидацию")
    #     print(form.errors)  # Вывод ошибок валидации
    #     return super().form_invalid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if "message" in form.fields:
            del form.fields["message"]
        if "recaptcha" in form.fields:
            del form.fields["recaptcha"]
        return form


class CustomLoginView(LoginView):
    form_class = UserLoginForm

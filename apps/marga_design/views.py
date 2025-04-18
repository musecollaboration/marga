from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from apps.marga_design.forms import AuthorForm
from apps.marga_design.models import Project, Application


# макет https://preview.colorlib.com/#marga
# https://colorlib.com/wp/templates/

class MargaHome(ListView):
    """
    Главная страница сайта
    """
    model = Project
    template_name = 'marga_design/home.html'
    context_object_name = 'projects_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(top_rating=True).order_by('?')[:4]
        return queryset


class MargaProject(DetailView):
    """
    Страница проекта
    """
    model = Project
    template_name = 'marga_design/project.html'
    context_object_name = 'project'


class MargaProjectsList(ListView):
    """
    Страница со всеми проектами
    """
    model = Project
    template_name = 'marga_design/projects_list.html'
    context_object_name = 'projects_list'
    paginate_by = 6
    queryset = Project.objects.filter(published=True)


class MargaProjectsApplicationCreateView(CreateView):
    """
    Форма для создания заявки на проект
    """
    model = Application
    template_name = 'marga_design/application_form.html'
    form_class = AuthorForm
    success_url = reverse_lazy('marga_design:thanks')


    def form_valid(self, form):
        form.instance.answer = Application.NEW
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     print("Форма не прошла валидацию:", form.errors)
    #     return super().form_invalid(form)


class MargaContactCreateView(CreateView):
    """
    Страница с формой обратной связи
    """
    model = Application
    template_name = 'marga_design/contact.html'
    form_class = AuthorForm
    success_url = reverse_lazy('marga_design:thanks')

    def form_valid(self, form):
        form.instance.answer = Application.NEW
        return super().form_valid(form)
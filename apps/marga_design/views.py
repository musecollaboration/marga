from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.marga_design.models import Project


# макет https://preview.colorlib.com/#marga
# https://colorlib.com/wp/templates/

class MargaHome(ListView):
    model = Project
    template_name = 'marga_design/home.html'
    context_object_name = 'projects_list'


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(top_rating=True).order_by('?')[:4]
        return queryset


class MargaProject(DetailView):
    model = Project
    template_name = 'marga_design/project.html'
    context_object_name = 'project'


class MargaProjectsList(ListView):
    model = Project
    template_name = 'marga_design/projects_list.html'
    context_object_name = 'projects_list'
    paginate_by = 6
    queryset = Project.objects.filter(published=True)
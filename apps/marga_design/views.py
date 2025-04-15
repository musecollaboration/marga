from django.shortcuts import render
from django.views.generic import ListView

from apps.marga_design.models import Project


# макет https://preview.colorlib.com/#marga
# https://colorlib.com/wp/templates/

class MargaHome(ListView):
    model = Project
    template_name = 'marga_design/home.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        return Project.objects.all()





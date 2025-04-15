from django.shortcuts import render
from django.views.generic import ListView

from apps.marga_design.models import Project


# макет https://preview.colorlib.com/#marga
# https://colorlib.com/wp/templates/

class MargaProject(ListView):
    model = Project




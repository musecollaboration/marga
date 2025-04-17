from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'marga_design'
urlpatterns = [
    path('', views.MargaHome.as_view(template_name='marga_design/home.html'), name='index'),

    path('projects/', views.MargaProjectsList.as_view(), name='projects_list'),
    path('project<slug:slug>/', views.MargaProject.as_view(), name='project'),
    path('application/', views.MargaProjectsApplicationCreateView.as_view(), name='application'),
    path('thanks/', TemplateView.as_view(template_name='marga_design/thanks.html'), name='thanks'),
]

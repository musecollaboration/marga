from django.urls import path

from . import views

app_name = 'marga_design'
urlpatterns = [
    path('', views.MargaHome.as_view(template_name='marga_design/home.html'), name='index'),
]

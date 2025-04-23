from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'marga_design'
urlpatterns = [

    path('projects/', views.MargaProjectsList.as_view(), name='projects_list'),
    path('project/<slug:slug>/', views.MargaProject.as_view(), name='project'),

    path('application/', views.MargaProjectsApplicationCreateView.as_view(), name='application'),
    path('thanks/', TemplateView.as_view(template_name='marga_design/thanks.html'), name='thanks'),
    path('services/', TemplateView.as_view(template_name='marga_design/services.html'), name='services'),
    path('about/', TemplateView.as_view(template_name='marga_design/about.html'), name='about'),
    path('contact/', views.MargaContactCreateView.as_view(template_name='marga_design/contact.html'), name='contact'),
    path("blog/", views.BlogListView.as_view(), name="blog_list"),
    path("blog/<slug:slug>/edit/", views.BlogPostEditView.as_view(), name="blog_edit"),
    path("blog/create/", views.CreateBlogPost.as_view(), name="create_blog_post"),
    path("blog/<slug:slug>/", views.BlogPostDetailView.as_view(), name="blog_post"),
    path('', views.MargaHome.as_view(template_name='marga_design/home.html'), name='index'),
]

from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path('user/<slug:slug>/', views.ProfilePage.as_view(), name='user'),
    path('application/<int:pk>/', views.ApplicationUpdateView.as_view(), name='user_answer'),
    path('login/', views.CustomLoginView.as_view(template_name='user_management/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='marga_design:index'), name='logout'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('registration_success/', views.registration_success_view, name='registration_success'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('monthly_dashboard/', views.monthly_dashboard_view, name='monthly_dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('mini_statement/', views.mini_statement_view, name='mini_statement'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact_view, name='contact'),
]
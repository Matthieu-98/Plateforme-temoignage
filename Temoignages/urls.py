"""
URL configuration for Temoignages project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('index/', views.index, name='index'),
    path('creation/', views.creation, name='creation'),
    path('questionnaire/', views.questionnaires, name='questionnaires'),
    path('questionnaire/create/', views.create_questionnaire, name='create_questionnaire'),
    path('questionnaire/questionnaires_prives/', views.questionnaires_prives, name='questionnaires_prives'),
    path('questionnaire/questionnaires_publics/', views.questionnaires_publics, name='questionnaires_publics'),
    path('droits/', views.droits, name='droits'),
    path('langues/', views.langues, name='langues'),
    path('sign/', views.sign, name='sign'),
    path('sign/register/', views.register, name='register'),
    path('sign/forgotten-password/', views.forgotten_password, name='forgotten_password'),
    path('temoignage/', views.temoignage, name = 'temoignage'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('send-link/', views.send_confirmation_link, name='send_link'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset/<uidb64>/<token>/', views.set_new_password, name='set_new_password'),

]

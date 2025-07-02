from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Accueil
    path('', views.index, name='index'),
    path('index/', views.index),  

    # Authentification personnalisée
    path('login/', views.login_register, name='login'),  
    path('register/', views.login_register, name='register'), 
    path('login/forgotten-password/', views.forgotten_password, name='forgotten_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset/<uidb64>/<token>/', views.set_new_password, name='set_new_password'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Création de questionnaires
    path('creation/', views.creation, name='creation'),
    path('questionnaires/', views.questionnaires, name='questionnaires'),
    path('questionnaires/create/', views.create_questionnaire, name='create_questionnaire'),
    path('questionnaires/prives/', views.questionnaires_prives, name='questionnaires_prives'),
    path('questionnaires/publics/', views.questionnaires_publics, name='questionnaires_publics'),

    # Témoignages
    path('temoignage/', views.temoignage_upload, name='temoignage_upload'),
    path('temoins/', views.liste_temoin, name='liste_temoin'),

    # Divers
    path('upload-test/', views.upload_test, name='upload_test'),

]


# Fichiers médias 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

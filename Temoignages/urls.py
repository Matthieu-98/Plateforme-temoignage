from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Page d'accueil
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('login/forgotten-password/', views.forgotten_password, name='forgotten_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset/<uidb64>/<token>/', views.set_new_password, name='set_new_password'),
    path('send-link/', views.login_register, name='send_link'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Création et gestion de questionnaires
    path('creation/', views.creation, name='creation'),
   # path('create/', views.create_questionnaire, name='create_questionnaire'),
    path('questionnaire/', views.questionnaires, name='questionnaires'),
    path('questionnaire/create/', views.create_questionnaire, name='create_questionnaire'),
    path('questionnaire/questionnaires_prives/', views.questionnaires_prives, name='questionnaires_prives'),
    path('questionnaire/questionnaires_publics/', views.questionnaires_publics, name='questionnaires_publics'),

    # Témoignages
    path('temoignage/', views.temoignage_upload, name='temoignage_upload'),
    path('temoins/', views.liste_temoin, name='liste_temoin'),

    # Divers
    path('langues/', views.langues, name='langues'),
    path('upload-test/', views.upload_test, name='upload_test'),
]

# Fichiers médias (en mode développement)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
import json

from .models import Temoin, Questionnaire, Question
from .forms import LoginForm

# -------------------------
# Pages statiques / templates simples
# -------------------------

def index(request):
    return render(request, 'index.html')

def questionnaires(request):
    return render(request, 'questionnaires.html')

def questionnaires_publics(request):
    return render(request, 'questionnaires_publics.html')

def langues(request):
    return render(request, 'langues.html')

def login_view(request):
    return render(request, 'login_register.html')

def register(request):
    return render(request, 'register.html')

def creation(request):
    return render(request, 'create.html')

def forgotten_password(request):
    return render(request, 'forgotten_password.html')

def temoignage(request):
    return render(request, 'temoignage.html')

# -------------------------
# Connexion personnalisée avec formulaire
# -------------------------
User = get_user_model()

def login_register(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action not in ['login', 'register']:
            return HttpResponseBadRequest("Action invalide.")

        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirmation = request.POST.get('confirmation', '')

        if action == 'login':
            user = authenticate(request, username=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Connexion réussie.")
                    return redirect('index')
                else:
                    messages.warning(request, "Votre compte n'est pas encore activé.")
            else:
                messages.error(request, "Identifiants invalides.")

        elif action == 'register':
            if not email or not password or not confirmation:
                messages.error(request, "Tous les champs sont obligatoires.")
            elif password != confirmation:
                messages.error(request, "Les mots de passe ne correspondent pas.")
            elif User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                messages.error(request, "Un compte avec cet e-mail existe déjà.")
            else:
                user = User.objects.create_user(username=email, email=email, password=password)
                user.is_active = False
                user.save()

                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                confirmation_url = f"http://{current_site.domain}/activate/{uid}/{token}/"

                message = render_to_string("emails/activation_email.html", {
                    'user': user,
                    'confirmation_url': confirmation_url,
                })

                try:
                    mail = EmailMessage(
                        subject="Confirmez votre adresse e-mail",
                        body=message,
                        to=[email],
                    )
                    mail.content_subtype = 'html'
                    mail.send()
                    messages.success(request, "Un e-mail de confirmation vous a été envoyé.")
                except Exception as e:
                    messages.error(request, "Erreur lors de l’envoi de l’e-mail. Veuillez réessayer plus tard.")

                return redirect('login')  

    return render(request, 'login_register.html')

# -------------------------
# Réinitialisation du mot de passe
# -------------------------

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                messages.error(request, "Ce compte n'est pas encore activé.")
                return redirect('reset_password')

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            reset_url = f"http://{current_site.domain}/reset/{uid}/{token}/"

            message = render_to_string("emails/password_reset_email.html", {
                'user': user,
                'reset_url': reset_url,
            })

            mail = EmailMessage(
                subject="Réinitialisation de votre mot de passe",
                body=message,
                to=[email]
            )
            mail.content_subtype = 'html'
            mail.send()

            messages.success(request, "Un e-mail de réinitialisation a été envoyé.")
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, "Aucun compte associé à cette adresse e-mail.")

    return render(request, 'reset_password.html')

def set_new_password(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm = request.POST.get('confirm')
            if password != confirm:
                return render(request, 'set_new_password.html', {
                    'error': "Les mots de passe ne correspondent pas.",
                    'uidb64': uidb64,
                    'token': token,
                })
            user.set_password(password)
            user.save()
            messages.success(request, "Votre mot de passe a été mis à jour. Vous pouvez maintenant vous connecter.")
            return redirect('login')
        return render(request, 'set_new_password.html', {
            'uidb64': uidb64,
            'token': token,
        })
    else:
        return HttpResponse("Lien de réinitialisation invalide ou expiré.")

# -------------------------
# Activation du compte via email
# -------------------------

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            message = "Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter."
        else:
            message = "Votre compte est déjà activé."
        return render(request, "emails/activation_success.html", {"message": message})
    else:
        return render(request, "emails/activation_failed.html", {"message": "Lien de confirmation invalide ou expiré."})

# -------------------------
# Gestion des témoignages
# -------------------------

@login_required
def liste_temoin(request):
    temoins = Temoin.objects.select_related('questionnaire').order_by('-date_creation')
    return render(request, 'temoignage.html', {'temoins': temoins})

@login_required
def temoignage_upload(request):
    if request.method == 'POST':
        questionnaire_id = request.POST.get('questionnaire_id')
        video_file = request.FILES.get('videoUpload')

        if questionnaire_id and video_file:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
            Temoin.objects.create(
                questionnaire=questionnaire,
                utilisateur=request.user,
                fichier_video=video_file
            )
            return redirect('liste_temoin')

    questionnaires = Questionnaire.objects.filter(utilisateur=request.user)
    return render(request, 'temoignage_upload.html', {
        'questionnaires': questionnaires
    })

@login_required
def upload_test(request):
    if request.method == "POST":
        video = request.FILES.get("video")  
        questionnaire_id = request.POST.get("questionnaire")  

        if not video or not questionnaire_id:
            messages.error(request, "Tous les champs sont obligatoires.")
            return redirect("upload_test")

        try:
            questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
        except Questionnaire.DoesNotExist:
            messages.error(request, "Questionnaire invalide.")
            return redirect("upload_test")

        Temoin.objects.create(
            utilisateur=request.user,
            questionnaire=questionnaire,
            fichier_video=video,
        )

        messages.success(request, "Vidéo envoyée avec succès.")
        return redirect("liste_temoin")

    questionnaires = Questionnaire.objects.all()
    return render(request, "upload_test.html", {"questionnaires": questionnaires})

# -------------------------
# Création de questionnaire via AJAX POST JSON
# -------------------------

@require_POST
@login_required
def create_questionnaire(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentification requise.'}, status=401)

    print("Requête reçue à create_questionnaire")
    print("Utilisateur connecté :", request.user)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides.'}, status=400)

    title = data.get('title', '').strip()
    is_public = data.get('is_public', False)
    questions = data.get('questions', [])

    if not title:
        return JsonResponse({'error': 'Le titre du questionnaire est obligatoire.'}, status=400)

    if not isinstance(questions, list) or not all(isinstance(q, dict) for q in questions):
        return JsonResponse({'error': 'Format des questions invalide.'}, status=400)

    # Création du questionnaire
    questionnaire = Questionnaire.objects.create(
        titre=title,
        utilisateur=request.user,
        is_public=is_public
    )

    print(f"Questionnaire créé : ID={questionnaire.id}, titre='{questionnaire.titre}', public={questionnaire.is_public}")

    # Création des questions
    for q in questions:
        texte = q.get('texte', '').strip()
        is_required = q.get('is_required', False)

        if texte:
            Question.objects.create(
                questionnaire=questionnaire,
                texte=texte,
                is_required=is_required
            )

    return JsonResponse({'message': 'Questionnaire créé avec succès.'})

# -------------------------
# Liste des questionnaires privés de l'utilisateur
# -------------------------

@login_required
def questionnaires_prives(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    questionnaires = Questionnaire.objects.filter(utilisateur=request.user)
    print(f"Questionnaires pour {request.user}: {questionnaires}")
    return render(request, 'questionnaires_prives.html', {'questionnaires': questionnaires})

# -------------------------
# Liste des questionnaires publics de l'utilisateur
# -------------------------

def questionnaires_publics(request):
    # On récupère uniquement les questionnaires publics
    questionnaires = Questionnaire.objects.filter(is_public=True).order_by('-date_creation')
    print(f"Questionnaires publics : {questionnaires}")
    return render(request, 'questionnaires_publics.html', {'questionnaires': questionnaires})
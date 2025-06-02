from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from .models import Temoin
from django.http import JsonResponse
import json
from .models import Questionnaire, Question
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'Temoignages/index.html')

def questionnaires(request):
    return render(request, 'Temoignages/questionnaires.html')

def questionnaires_publics(request):
    return render(request, 'Temoignages/questionnaires_publics.html')

def questionnaires_prives(request):
    return render(request, 'Temoignages/questionnaires_prives.html')

def droits(request):
    return render(request, 'Temoignages/droits.html')

def langues(request):
    return render(request, 'Temoignages/langues.html')

def sign(request):
    return render(request, 'Temoignages/sign.html')

def register(request):
    return render(request, 'Temoignages/register.html')

def creation(request):
    return render(request, 'Temoignages/create.html')

def forgotten_password(request):
    return render(request, 'Temoignages/forgotten_password.html')

def reset_password(request):
    return render(request, 'Temoignages/reset_password.html')

def temoignage(request):
    return render(request, 'Temoignages/temoignage.html')


def send_confirmation_link(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("mot_de_passe")
        confirmation = request.POST.get("confirmation")

        if password != confirmation:
            return HttpResponse("Les mots de passe ne correspondent pas.")

        if User.objects.filter(username=email).exists():
            return HttpResponse("Un utilisateur avec cette adresse e-mail existe déjà.")

        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False  # Compte désactivé jusqu'à vérification

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        confirmation_url = f"http://{current_site.domain}/activate/{uid}/{token}/"

        message = render_to_string("emails/activation_email.html", {
            'user': user,
            'confirmation_url': confirmation_url,
        })

        mail = EmailMessage(
            subject="Confirmez votre adresse e-mail",
            body=message,
            to=[email],
        )
        mail.content_subtype = 'html'  
        mail.send()

        return HttpResponse("Un e-mail de confirmation vous a été envoyé.")

    return redirect('register')

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

def liste_temoin(request):
    temoins = Temoin.objects.select_related('questionnaire').order_by('-date_creation')
    return render(request, 'Temoignages/temoignage.html', {'temoins': temoins})

def create_questionnaire(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', '')
            questions = data.get('questions', [])

            # ➤ Enregistrement réel dans la base de données
            questionnaire = Questionnaire.objects.create(
                titre=title,
                utilisateur=request.user if request.user.is_authenticated else None
            )

            for q in questions:
                Question.objects.create(questionnaire=questionnaire, texte=q)

            return JsonResponse({'message': 'Questionnaire enregistré avec succès.'}, status=201)

        except Exception as e:
            print("❌ Erreur JSON:", e)
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def questionnaires_prives(request):
    if request.user.is_authenticated:
        questionnaires = Questionnaire.objects.filter(utilisateur=request.user).prefetch_related('questions')
    else:
        questionnaires = []
    return render(request, 'Temoignages/questionnaires_prives.html', {'questionnaires': questionnaires})


@csrf_protect
def custom_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect('sign')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Connexion réussie.")
                return redirect('index')
            else:
                messages.warning(request, "Votre compte n'est pas encore activé.")
                return redirect('sign')
        else:
            messages.error(request, "Identifiants invalides.")
            return redirect('sign')

    return render(request, 'Temoignages/sign.html')

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
            return redirect('sign')

        except User.DoesNotExist:
            messages.error(request, "Aucun compte associé à cette adresse e-mail.")

    return render(request, 'Temoignages/reset_password.html')

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
                return render(request, 'Temoignages/set_new_password.html', {
                    'error': "Les mots de passe ne correspondent pas.",
                    'uidb64': uidb64,
                    'token': token,
                })
            user.set_password(password)
            user.save()
            messages.success(request, "Votre mot de passe a été mis à jour. Vous pouvez maintenant vous connecter.")
            return redirect('sign')  # Redirige vers la page de connexion
        return render(request, 'Temoignages/set_new_password.html', {
            'uidb64': uidb64,
            'token': token,
        })
    else:
        return HttpResponse("Lien de réinitialisation invalide ou expiré.")

def upload_test(request):
    if request.method == 'POST':
        questionnaire_id = request.POST.get('questionnaire')
        video_file = request.FILES.get('video')

        if questionnaire_id and video_file:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
            Temoin.objects.create(
                questionnaire=questionnaire,
                fichier_video=video_file
            )
            return redirect('liste_temoin')  # redirige vers la page listant les témoignages

    questionnaires = Questionnaire.objects.all()
    return render(request, 'Temoignages/upload_test.html', {
        'questionnaires': questionnaires
    })
    
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
            return redirect('liste_temoin')  # Redirige vers la liste des témoignages

    questionnaires = Questionnaire.objects.filter(utilisateur=request.user)
    return render(request, 'Temoignages/temoignage_upload.html', {
        'questionnaires': questionnaires
    })

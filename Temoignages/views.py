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
    return render(request, 'Temoignages/creation.html')

def forgotten_password(request):
    return render(request, 'Temoignages/forgotten_password.html')

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

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Votre compte a été activé.")
    else:
        return HttpResponse("Lien de confirmation invalide.")
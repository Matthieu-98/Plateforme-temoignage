from django.db import models
# Create your models here.
# Temoignages/models.py
from django.contrib.auth.models import User

class Questionnaire(models.Model):
    titre = models.CharField(max_length=255)
    utilisateur = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date_creation = models.DateTimeField(auto_now_add=True)  


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, related_name="questions", on_delete=models.CASCADE)
    texte = models.CharField(max_length=500)
    
class Temoin(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    fichier_video = models.FileField(upload_to='uploads/')
    date_creation = models.DateTimeField(auto_now_add=True)

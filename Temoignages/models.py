from django.db import models

# Create your models here.
# Temoignages/models.py

from django.db import models
from django.contrib.auth.models import User

class Questionnaire(models.Model):
    titre = models.CharField(max_length=255)

    def __str__(self):
        return self.titre

class Temoin(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    fichier_video = models.FileField(upload_to='uploads/')
    date_creation = models.DateTimeField(auto_now_add=True)

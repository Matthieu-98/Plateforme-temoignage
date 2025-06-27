from django.db import models
from django.contrib.auth.models import User

class Questionnaire(models.Model):
    titre = models.CharField(max_length=255)
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questionnaires'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.titre

class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, related_name='questions', on_delete=models.CASCADE)
    texte = models.CharField(max_length=500)
    is_required = models.BooleanField(default=True)

    def __str__(self):
        return self.texte

class Temoin(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    fichier_video = models.FileField(upload_to="videos/")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Témoin du {self.date_creation} - {self.date_creation}"

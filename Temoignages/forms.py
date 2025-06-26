from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail", max_length=254)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

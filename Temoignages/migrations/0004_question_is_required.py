# Generated by Django 5.0.1 on 2025-06-09 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Temoignages', '0003_alter_temoin_fichier_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_required',
            field=models.BooleanField(default=True),
        ),
    ]

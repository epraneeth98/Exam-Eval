# Generated by Django 2.1.3 on 2018-11-27 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instructor', '0006_subjectiveexam_subjectiveexamtaken'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectiveexamtaken',
            name='corrected_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]

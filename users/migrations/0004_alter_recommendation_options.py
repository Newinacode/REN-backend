# Generated by Django 4.2.1 on 2024-02-16 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_recommendation_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recommendation',
            options={'ordering': ['-created_at']},
        ),
    ]

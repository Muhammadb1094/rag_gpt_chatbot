# Generated by Django 5.0.3 on 2024-03-09 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='last_message',
            field=models.TextField(default='No Last Message Found.'),
        ),
    ]

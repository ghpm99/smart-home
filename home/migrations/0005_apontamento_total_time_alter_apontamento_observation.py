# Generated by Django 4.2.3 on 2025-03-20 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_apontamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apontamento',
            name='observation',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]

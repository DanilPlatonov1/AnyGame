# Generated by Django 5.0.6 on 2024-05-21 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_report_delete_complaint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.profile'),
        ),
    ]
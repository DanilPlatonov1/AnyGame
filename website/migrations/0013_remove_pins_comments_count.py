# Generated by Django 5.0.6 on 2024-05-31 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_pins_comments_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pins',
            name='comments_count',
        ),
    ]

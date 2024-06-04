# Generated by Django 5.0.6 on 2024-05-15 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_pins_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.profile')),
                ('pin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.pins')),
            ],
        ),
    ]
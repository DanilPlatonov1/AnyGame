# Generated by Django 5.0.6 on 2024-05-31 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_delete_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='pins',
            name='comments_count',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-04 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_profile_is_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collections',
            name='collection_image',
            field=models.ImageField(default='collections/favorites.jpg', upload_to='collections/'),
        ),
    ]
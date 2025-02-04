# Generated by Django 4.2.11 on 2024-04-06 18:18

import chronicled.profiles.models
import chronicled.profiles.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='images/anon-user.webp', null=True, upload_to=chronicled.profiles.models.profile_picture_path, validators=[chronicled.profiles.validators.validate_file_size]),
        ),
    ]

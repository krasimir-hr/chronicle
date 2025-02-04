# Generated by Django 5.0.3 on 2024-03-28 11:46

import chronicled.profiles.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/profile-pictures', validators=[chronicled.profiles.validators.validate_file_size]),
        ),
    ]

from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from .models import Profile, AppUser

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=AppUser)
def delete_user_avatar(sender, instance, **kwargs):
    try:
        profile = Profile.objects.get(user=instance)
        if profile.profile_picture:
            profile.profile_picture.delete()
    except Profile.DoesNotExist:
        pass

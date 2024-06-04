from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Profile


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    profile.is_online = True
    profile.save()


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    try:
        profile = Profile.objects.get(user=user)
        profile.is_online = False
        profile.save()
    except Profile.DoesNotExist:
        pass

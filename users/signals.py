from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, BarberProfile

@receiver(post_save, sender=BarberProfile)
def barber_profile_saved(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.user.pk)
        user.has_barber_profile = True
        user.save()


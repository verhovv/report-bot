from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def handle_new_model_instance(sender, instance, created, **kwargs):
    if created:
        print(f"Создана новая запись {instance}")

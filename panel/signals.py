from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver

from panel.models import Template, Publication
from panel.tasks import send_publication


@receiver(post_save, sender=Publication)
def handle_publication_save(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: send_publication.delay(instance.id))

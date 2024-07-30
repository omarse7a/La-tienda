from django.db.models.signals import post_delete
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from .models.bag_models import Bag

# handles deleting the unordered bags when their session expires
@receiver(post_delete, sender=Session)
def delete_expired_unordered_bags(sender, instance, **kwargs):
    Bag.objects.filter(session_key=instance.session_key, ordered=False).delete()
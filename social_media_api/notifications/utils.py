from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(actor, recipient, verb, target=None):
    content_type = ContentType.objects.get_for_model(target) if target else None
    object_id = target.id if target else None
    Notification.objects.create(
        actor=actor,
        recipient=recipient,
        verb=verb,
        content_type=content_type,
        object_id=object_id
    )

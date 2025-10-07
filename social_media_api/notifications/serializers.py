from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_id = serializers.IntegerField(source='object_id', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'actor_username', 'verb', 'target_id', 'is_read', 'timestamp']

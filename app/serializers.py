from rest_framework import serializers
from .models import BotStatus

class BotStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotStatus
        fields = '__all__'


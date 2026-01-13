from rest_framework import serializers

class RebalanceResultSerializer(serializers.Serializer):
    total_value = serializers.FloatField()
    actions = serializers.ListField()

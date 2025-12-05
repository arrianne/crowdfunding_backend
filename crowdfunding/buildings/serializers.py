# buildings/serializers.py
from rest_framework import serializers
from .models import Building


class BuildingSerializer(serializers.ModelSerializer):
    # owner is read-only, set from request.user in the view
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Building
        fields = '__all__'



from rest_framework import serializers
from .models import Building, BuildingMembership

class BuildingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Building
        fields = '__all__'


class BuildingMembershipSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = BuildingMembership
        fields = '__all__'

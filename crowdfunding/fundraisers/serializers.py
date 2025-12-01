from rest_framework import serializers
from django.apps import apps
from .models import Fundraiser, Pledge #Referencing the model class directly since adding extra logic below for pledge type.


##############################################
#Pledge serializers 
##############################################

class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='supporter.id')

    pledge_type = serializers.ChoiceField(
        choices=Pledge.PledgeType.choices,
        default=Pledge.PledgeType.MONEY,
    )
    amount = serializers.IntegerField(required=False, allow_null=True)
    skill_description = serializers.CharField(required=False, allow_blank=True)
    hours = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Pledge
        fields = '__all__'

    def validate(self, attrs):
        """
        Enforce:
        - Money pledge → amount required
        - Skill pledge → skill_description required
        """

        # Support both create (attrs only) and update (self.instance + attrs)
        pledge_type = attrs.get('pledge_type')
        if self.instance and pledge_type is None:
            pledge_type = self.instance.pledge_type

        amount = attrs.get('amount')
        if self.instance and amount is None:
            amount = self.instance.amount

        skill_description = attrs.get('skill_description')
        if self.instance and skill_description is None:
            skill_description = self.instance.skill_description

        if pledge_type == Pledge.PledgeType.MONEY:
            if amount is None:
                raise serializers.ValidationError({
                    "amount": "Money pledges must include an amount."
                })

        elif pledge_type == Pledge.PledgeType.SKILL:
            if not skill_description:
                raise serializers.ValidationError({
                    "skill_description": "Skill pledges must include a skill description."
                })

        else:
            # Safety net: shouldn't really happen because of ChoiceField,
            # but it's nice to be explicit.
            raise serializers.ValidationError({
                "pledge_type": "Invalid pledge type."
            })

        return attrs


#############################################
#Fundraiser serializers 
#############################################*

class FundraiserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    # The only thing we need to do is specify which model to convnert and which fields it should include below.
    class Meta:
        model = apps.get_model('fundraisers.Fundraiser')
        fields = '__all__'

class FundraiserDetailSerializer(FundraiserSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

def update(self, instance, validated_data):
    instance.title = validated_data.get('title', instance.title)
    instance.description = validated_data.get('description', instance.description)
    instance.goal = validated_data.get('goal', instance.goal)
    instance.image = validated_data.get('image', instance.image)
    instance.is_open = validated_data.get('is_open', instance.is_open)
    instance.date_created = validated_data.get('date_created', instance.date_created)
    instance.owner = validated_data.get('owner', instance.owner)
    instance.save()
    return instance
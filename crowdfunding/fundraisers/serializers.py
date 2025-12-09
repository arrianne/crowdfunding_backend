from rest_framework import serializers
from .models import Fundraiser, Pledge


##############################################
# Pledge serializer
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
        - Money pledge → amount required (and positive)
        - Skill pledge → skill_description required
        - Block ALL *new* pledges (money + skill) once goal is reached or fundraiser is closed.
        """

        # ---- Resolve pledge_type, amount, skill_description for create + update ----
        pledge_type = attrs.get('pledge_type')
        if self.instance and pledge_type is None:
            pledge_type = self.instance.pledge_type

        amount = attrs.get('amount')
        if self.instance and amount is None:
            amount = self.instance.amount

        skill_description = attrs.get('skill_description')
        if self.instance and skill_description is None:
            skill_description = self.instance.skill_description

        # ---- Resolve fundraiser ----
        fundraiser = attrs.get('fundraiser')
        if self.instance and fundraiser is None:
            fundraiser = self.instance.fundraiser

        if not fundraiser:
            raise serializers.ValidationError({
                "fundraiser": "A fundraiser must be specified for this pledge."
            })

        # ---- Block new pledges if goal reached / fundraiser closed ----
        # Only for CREATE so you can still edit existing pledges if needed.
        
        if fundraiser.is_funded or not fundraiser.is_open:
            raise serializers.ValidationError(
                "This fundraiser has reached its goal and is no longer accepting pledges."
            )

        # ---- Base validations: money vs skill ----
        if pledge_type == Pledge.PledgeType.MONEY:
            if amount is None:
                raise serializers.ValidationError({
                    "amount": "Money pledges must include an amount."
                })
            if amount <= 0:
                raise serializers.ValidationError({
                    "amount": "Money pledges must be a positive amount."
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
# Fundraiser serializers
#############################################

class FundraiserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    total_pledged = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    # read-only goal reached flag
    is_funded = serializers.ReadOnlyField()

    class Meta:
        model = Fundraiser
        fields = '__all__'
        # You don't actually need extra_fields here; DRF will include
        # total_pledged and progress_percent automatically because they are declared.

    def get_total_pledged(self, obj):
        # Use the model helper so there's a single source of truth
        return obj.total_pledged

    def get_progress_percent(self, obj):
        total = obj.total_pledged
        if obj.goal and obj.goal > 0:
            return round((total / obj.goal) * 100, 2)
        return 0

    # If you really want a custom update (you don't *have* to override)
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


class FundraiserDetailSerializer(FundraiserSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

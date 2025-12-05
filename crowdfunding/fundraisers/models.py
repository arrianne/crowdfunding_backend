from django.db import models
from django.contrib.auth import get_user_model



#############################################
#Fundraiser model 
#############################################


class Fundraiser(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_fundraisers'
    )

    # NEW: link to Building
    building = models.ForeignKey(
        'buildings.Building',         # app_label.ModelName
        on_delete=models.CASCADE,
        related_name='fundraisers'
    )


    def __str__(self):
        return f"{self.title} — owner: {self.owner.username}"



#############################################
#Pledge model with two types: Money and Skill
#############################################

class Pledge(models.Model):
    class PledgeType(models.TextChoices):
        MONEY = 'MONEY', 'Money'
        SKILL = 'SKILL', 'Skill'

    pledge_type = models.CharField(
        max_length=10,
        choices=PledgeType.choices,
        default=PledgeType.MONEY,
    )

    # Money pledge fields
    amount = models.IntegerField(null=True, blank=True)

    # Skill pledge fields
    skill_description = models.CharField(max_length=200, blank=True)
    hours = models.IntegerField(null=True, blank=True)

    # Common fields
    comment = models.CharField(max_length=200, blank=True)
    anonymous = models.BooleanField(default=False)

    fundraiser = models.ForeignKey(
        'Fundraiser',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pledges_made'
    )
    # this turns internal DB values into friendly text
    def __str__(self):
        return f"{self.get_pledge_type_display()} pledge to {self.fundraiser.title}"

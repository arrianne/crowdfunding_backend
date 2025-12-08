from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum



#############################################
#Fundraiser model 
#############################################


class Fundraiser(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField(default=True)
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
        related_name='fundraisers',

    )

    def __str__(self):
        return f"{self.title} — owner: {self.owner.username}"

    # HELPER PROPERTIES FOR FUNDRAISER MODEL

    # self.pledges uses related_name='pledges' on Pledge.fundraiser.
    # Sum('amount') will ignore NULL amounts, so pure skill pledges don’t break anything.

    # Total money pledged (ignores skill-only pledges because amount is null)
    @property
    def total_pledged(self):
        result = self.pledges.aggregate(total=Sum('amount'))['total']
        return result or 0

    # Percentage of goal reached
    @property
    def progress_percentage(self):
        if self.goal and self.goal > 0:
            return round((self.total_pledged / self.goal) * 100, 1)
        return 0
    
    # has this fundraiser hit or passed its goal?
    @property
    def is_funded(self):
        return self.total_pledged >= self.goal
    


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

from django.db import models
from django.conf import settings

# Create your models here.


class Building(models.Model):
    """
    A strata building / body corporate.
    """
    name = models.CharField(max_length=255)
    cts_number = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo = models.URLField(blank=True, null=True)


    # Who owns / administers this building in the system
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_buildings'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#############################################
#BuildingMembership model
#############################################

# represents the relationship between a user and a building

class BuildingMembership(models.Model):
    """
    A user belonging to a building in some role
    (committee, resident, tradie, etc).
    """
    COMMITTEE = 'committee'
    RESIDENT = 'resident'
    TRADIE = 'tradie'

    ROLE_CHOICES = [
        (COMMITTEE, 'Committee Member'),
        (RESIDENT, 'Resident'),
        (TRADIE, 'Tradesperson'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='building_memberships'
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'building')

    def __str__(self):
        return f"{self.user} → {self.building} ({self.role})"

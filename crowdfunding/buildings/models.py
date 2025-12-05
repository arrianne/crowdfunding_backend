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



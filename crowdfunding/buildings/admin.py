from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Building, BuildingMembership

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'address')


@admin.register(BuildingMembership)
class BuildingMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'building', 'role', 'joined_at')
    list_filter = ('role', 'building')
    search_fields = ('user__username', 'building__name')

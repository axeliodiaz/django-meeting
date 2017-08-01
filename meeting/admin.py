from django.contrib import admin

from .models import Supplie, Room, Reservation


class RoomAdmin(admin.ModelAdmin):
    """docstring for SupplieAdmin."""
    list_filter = ['name', 'capacity', 'supplie']
    list_display = ['name', 'capacity']
    search_fields = ['name', 'supplie']


class ReservationAdmin(admin.ModelAdmin):
    """docstring for SupplieAdmin."""
    list_filter = ['room__status', 'supplie']
    list_display = ['room', 'date', 'start', 'end']
    search_fields = ['room__name']


class SupplieAdmin(admin.ModelAdmin):
    """docstring for SupplieAdmin."""
    list_filter = ['name', 'room']
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Supplie, SupplieAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Room, RoomAdmin)

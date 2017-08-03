from django.contrib import admin

from .models import Supplie, Room, Reservation, ReservationRequest


class RoomAdmin(admin.ModelAdmin):
    """docstring for RoomAdmin."""
    list_filter = ['name', 'capacity', 'status', 'supplie']
    list_display = ['name', 'status', 'capacity']
    search_fields = ['name', 'supplie']


class ReservationAdmin(admin.ModelAdmin):
    """docstring for ReservationAdmin."""
    list_filter = ['room__status', 'supplie', 'date', 'start', 'end']
    list_display = ['room', 'date', 'start', 'end']
    search_fields = ['room__name']


class SupplieAdmin(admin.ModelAdmin):
    """docstring for SupplieAdmin."""
    list_filter = ['name', 'room']
    list_display = ['name']
    search_fields = ['name']


class ReservationRequestAdmin(admin.ModelAdmin):
    """docstring for ReservationRequestAdmin."""
    list_filter = ['reservation__date']
    list_display = ['reservation', 'user']
    search_fields = ['reservation__room__name']


admin.site.register(Room, RoomAdmin)
admin.site.register(Supplie, SupplieAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservationRequest, ReservationRequestAdmin)

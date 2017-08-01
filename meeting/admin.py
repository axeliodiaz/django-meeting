from django.contrib import admin

from .models import Supplie, Room, Reservation


class RoomAdmin(admin.ModelAdmin):
    """docstring for SupplieAdmin."""
    list_filter = ['name', 'capacity', 'supplie']
    list_display = ['name', 'capacity']


admin.site.register(Supplie)
admin.site.register(Reservation)
admin.site.register(Room, RoomAdmin)

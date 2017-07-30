from django.shortcuts import render
from django.views.generic import ListView
from .models import Room


class RoomListView(ListView):
    model = Room
    template_name = "meeting/dashboard.html"
    paginate_by = 10
    context_object_name = "rooms"

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        return Room.objects.filter(
        ).order_by(
        )

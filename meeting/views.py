from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from .models import Room
from .forms import RoomForm

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "meeting/meeting_list.html"
    paginate_by = 10
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.filter(
        ).order_by(
        )


class RoomEditView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")

    def get_object(self, queryset=None):
        obj = Room.objects.get(id=self.kwargs['id'])
        return obj


class RoomCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")


class RoomDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")

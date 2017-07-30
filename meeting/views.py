from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from .models import Room, Supplie
from .forms import RoomForm, SupplieForm

from braces.views import (LoginRequiredMixin, SuperuserRequiredMixin,
                          MessageMixin)


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "meeting/meeting_list.html"
    paginate_by = 10
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.filter(
        ).order_by(
        )


class RoomEditView(MessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                   UpdateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")

    def get_object(self, queryset=None):
        obj = Room.objects.get(id=self.kwargs['pk'])
        return obj


class RoomCreateView(MessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                     CreateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")


class RoomDeleteView(MessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                     DeleteView):
    model = Room
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SupplieListView(LoginRequiredMixin, ListView):
    model = Supplie
    template_name = "meeting/supplie_list.html"
    paginate_by = 10
    context_object_name = "supplies"

    def get_queryset(self):
        return Supplie.objects.filter(
        ).order_by(
        )


class SupplieEditView(MessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                      UpdateView):
    template_name = 'meeting/supplie_edit.html'
    form_class = SupplieForm
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was saved successfully.")

    def get_object(self, queryset=None):
        obj = Supplie.objects.get(id=self.kwargs['pk'])
        return obj


class SupplieCreateView(MessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                        CreateView):
    template_name = 'meeting/supplie_edit.html'
    form_class = SupplieForm
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was saved successfully.")


class SupplieDeleteView(MessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                        DeleteView):
    model = Supplie
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was saved successfully.")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

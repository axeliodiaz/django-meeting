from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import (UpdateView, CreateView, DeleteView,
                                       FormMixin)
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.template.defaultfilters import urlencode
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Room, Supplie
from .forms import RoomForm, SupplieForm, SearchRoomForm

from braces.views import (LoginRequiredMixin, SuperuserRequiredMixin)


class FormListView(FormMixin, ListView):

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        orders = ['capacity']
        data = {'capacity__gte': self.request.POST.get('capacity', '')}

        if 'name' in self.request.POST:
            data.update({'name': self.request.POST.get('name')})
            orders.append('name')
        if 'location' in self.request.POST:
            data.update({'location': self.request.POST.get('location')})
            orders.append('location')
        if 'supplie' in self.request.POST:
            data.update({'supplie__in': self.request.POST.getlist('supplie', [])})
            orders.append('supplie')
        if data['capacity__gte'] == '':
            data['capacity__gte'] = 0
        return Room.objects.filter(**data).order_by(*orders)


class RoomListView(LoginRequiredMixin, FormListView):
    model = Room
    template_name = "meeting/meeting_list.html"
    paginate_by = 10
    context_object_name = "rooms"
    form_class = SearchRoomForm


class RoomEditView(SuccessMessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                   UpdateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")

    def get_object(self, queryset=None):
        obj = Room.objects.get(id=self.kwargs['pk'])
        return obj


class RoomCreateView(SuccessMessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                     CreateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")


class RoomDeleteView(SuccessMessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
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


class SupplieEditView(SuccessMessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                      UpdateView):
    template_name = 'meeting/supplie_edit.html'
    form_class = SupplieForm
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was saved successfully.")

    def get_object(self, queryset=None):
        obj = Supplie.objects.get(id=self.kwargs['pk'])
        return obj


class SupplieCreateView(SuccessMessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                        CreateView):
    template_name = 'meeting/supplie_edit.html'
    form_class = SupplieForm
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was saved successfully.")


class SupplieDeleteView(SuccessMessageMixin, LoginRequiredMixin, SuperuserRequiredMixin,
                        DeleteView):
    model = Supplie
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was saved successfully.")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

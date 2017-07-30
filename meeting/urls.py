from django.conf.urls import url
from django.contrib import admin
from .views import (RoomListView, RoomEditView, RoomCreateView, RoomDeleteView,
                    SupplieListView, SupplieEditView, SupplieCreateView,
                    SupplieDeleteView)


urlpatterns = [
    url(r'^(?P<pk>\d+)/change/', RoomEditView.as_view(), name='meeting_edit'),
    url(r'^(?P<pk>\d+)/delete/', RoomDeleteView.as_view(), name='meeting_delete'),
    url(r'^add/', RoomCreateView.as_view(), name='meeting_add'),
    url(r'^', RoomListView.as_view(), name='meeting_list'),
]

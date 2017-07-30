from django.conf.urls import url
from django.contrib import admin
from .views import (RoomListView, RoomEditView, RoomCreateView, RoomDeleteView,
                    SupplieListView, SupplieEditView, SupplieCreateView,
                    SupplieDeleteView)


urlpatterns = [
    url(r'^supplie/(?P<pk>\d+)/change/', SupplieEditView.as_view(), name='supplie_edit'),
    url(r'^supplie/(?P<pk>\d+)/delete/', SupplieDeleteView.as_view(), name='supplie_delete'),
    url(r'^supplie/add/', SupplieCreateView.as_view(), name='supplie_add'),
    url(r'^supplie/list/', SupplieListView.as_view(), name='supplie_list'),
    url(r'^(?P<pk>\d+)/change/', RoomEditView.as_view(), name='meeting_edit'),
    url(r'^(?P<pk>\d+)/delete/', RoomDeleteView.as_view(), name='meeting_delete'),
    url(r'^add/', RoomCreateView.as_view(), name='meeting_add'),
    url(r'^', RoomListView.as_view(), name='meeting_list'),
]

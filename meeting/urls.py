from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^', TemplateView.as_view(template_name='meeting/dashboard.html'),
        name='meeting_dashboard'),
]

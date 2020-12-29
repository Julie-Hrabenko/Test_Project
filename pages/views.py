from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class HomePagesView(TemplateView):
    template_name = 'home.html'


class AboutPagesView(TemplateView):
    template_name = 'about.html'


class ServicesPagesView(TemplateView):
    template_name = 'services.html'


class TeamPagesView(TemplateView):
    template_name = 'team.html'


class ContactPagesView(TemplateView):
    template_name = 'contact.html'



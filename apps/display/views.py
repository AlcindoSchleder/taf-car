# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render


class DisplayPageView(TemplateView):
    template_name = 'display/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

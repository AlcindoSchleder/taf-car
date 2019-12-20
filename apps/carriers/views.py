# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render


class CarriersPageView(TemplateView):
    template_name = 'carriers/carriers.html'

    def get(self, request, *args, **kwargs):
        levels = [2, 1]
        boxes = [1, 2, 3, 4, 5]
        return render(request, self.template_name, {"levels": levels, "boxes": boxes})

# -*- coding: utf-8 -*-
from django import forms
from .choices import CHARGES_OPTIONS, SORT_STRINGS_OPTIONS, SEPARATION_STRINGS_OPTIONS


class ClassificationChargesForm(forms.Form):
    pk_charges = forms.ChoiceField(
        choices=CHARGES_OPTIONS, label='Número da Carga', help_text='Número da Carga'
    )
    classification_mode = forms.ChoiceField(
        choices=SORT_STRINGS_OPTIONS,
        label='Modo de Classificaçáo', help_text='Modo de Classificaçáo'
    )
    separation_mode = forms.ChoiceField(
        choices=SEPARATION_STRINGS_OPTIONS,
        label='Modo de Separação', help_text='Modo de Separação'
    )

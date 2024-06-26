from django import forms
from django.forms import inlineformset_factory

from calculator.models import Client, Contact, Invoice

ContactFormSet = inlineformset_factory(Client, Contact, fields=('contact',), extra=1)



from django import forms
from django.forms import inlineformset_factory

from calculator.models import Client, Contact, Invoice

ContactFormSet = inlineformset_factory(Client, Contact, fields=('contact',), extra=1)


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'ktt', 'voltage', 'start', 'end']

import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView

from calculator.models import Client, Contact


# Create your views here.
@login_required
def index(request):
    return render(request, 'calculator/home.html')


class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    template_name = "calculator/create_client.html"
    success_url = "index"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return self.save_with_contacts(form)

    def save_with_contacts(self, form):
        contacts_array = self.request.POST.get('contacts_array', None)
        if contacts_array:
            client_instance = form.save(commit=False)
            client_instance.save()
            self.create_contacts_from_json(client_instance, contacts_array)
        else:
            form.save()
        return super().form_valid(form)

    def create_contacts_from_json(self, client_instance, json_data):
        contacts_array = json.loads(json_data)
        for contact_data in contacts_array:
            contact = Contact.objects.create(client=client_instance, contact=contact_data['phone'])


class ClientListView(ListView):
    model = Client
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.all()

    template_name = 'calculator/clients.html'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from .models import Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['name', 'sftp_host', 'sftp_port', 'sftp_path']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/home.html'
    ordering = ['id']
    paginate_by = 25


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['name', 'sftp_host', 'sftp_port', 'sftp_path']


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = '/'


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'clients/about.html', context)

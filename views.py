from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse

from .models import Country
from .models import User

class CountryCreateView(CreateView):
	template_name='.html'
	model=Country
	fields = ['Id', 'Name']
	success_url=reverse_lazy('')


class CountryUpdateView(UpdateView):
	template_name='.html'
	model=Country
	fields = ['Id', 'Name']


class CountryDeleteView(DeleteView):
	template_name='.html'
	model=Country
	success_url=reverse_lazy('')


class CountryListView(generic.ListView):
	template_name = '.html'
	context_object_name = 'all_Country'
	def get_queryset(self):
		return Country.object.all


class UserCreateView(CreateView):
	template_name='.html'
	model=User
	fields = ['Country', 'FirstName', 'LastName', 'Email']
	success_url=reverse_lazy('')


class UserUpdateView(UpdateView):
	template_name='.html'
	model=User
	fields = ['Country', 'FirstName', 'LastName', 'Email']


class UserDeleteView(DeleteView):
	template_name='.html'
	model=User
	success_url=reverse_lazy('')


class UserListView(generic.ListView):
	template_name = '.html'
	context_object_name = 'all_User'
	def get_queryset(self):
		return User.object.all


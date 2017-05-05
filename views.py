from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse

from ./models import Country
from ./models import User

class CountryCreateView(CreateView):
	template_name='.html'
	model=Country
	fields = ['id', 'name']
	success_url=reverse_lazy('')


class UserCreateView(CreateView):
	template_name='.html'
	model=User
	fields = ['firstName', 'lastName', 'email', 'country']
	success_url=reverse_lazy('')


import os
from django.db import models


class Country(models.Model):	
	Id = models.CharField(max_length=3),
	Name = models.CharField(max_length=20),
class User(models.Model):
	Country = models.ForeignKey(Country, on_delete=models.CASCADE)
	FirstName = models.CharField(max_length=3, null=True)
	LastName = models.CharField(max_length=3),
	Email = models.EmailField(max_length=30),
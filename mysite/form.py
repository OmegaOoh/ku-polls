"""Module contains class for User Registration Form."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
	"""Override of UserCreationForm which added optional field for email."""

	email = forms.EmailField(
		required=False,
		help_text='Optional')
	class Meta:
		"""Meta class contains field, its labels and widgets to show in form."""

		model = User
		fields = ['username', 'email', 'password1', 'password2']

from django.contrib.auth import forms as auth_forms
from RecHumanos.models import *

class VoluntarioChangeForm(auth_forms.UserChangeForm):
	class Meta:
		model = Voluntario

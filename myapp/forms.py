from django import forms
from . import models


class Contact_Form(forms.ModelForm):
	class Meta:
		model= models.Contact_form_model
		fields= ['Name', 'Email', 'Contact', 'Message']

class File_Form(forms.ModelForm):
	class Meta:
		model= models.File_model
		fields= '__all__'

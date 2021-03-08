from django.db import models

# Create your models here.
class Contact_form_model(models.Model):
	U_id		= models.AutoField(auto_created=True, primary_key=True, unique = True, null=False)
	Name		= models.CharField(max_length=100)
	Email		= models.EmailField()
	Contact		= models.CharField(max_length=100)
	Message 	= models.TextField(max_length=1000)
	Date 		= models.CharField(max_length=100)
	File_status = models.IntegerField()
	class Meta:
		db_table = "Contact_us"


class File_model(models.Model):
	U		= models.ForeignKey(Contact_form_model, on_delete=models.CASCADE)
	File 	= models.FileField(upload_to='media/', blank=True, null=True)
	class Meta:
		db_table = "Files"

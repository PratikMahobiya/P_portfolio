from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . import forms
from . import models

from datetime import datetime
from twilio.rest import Client

# Create your views here.
def Index(request):
	# messages.add_message(request, messages.INFO, "Thank You.. ")
	return render(request, "index.html")

def Contact(request):
	if request.method == 'POST':
		c_form 		= forms.Contact_Form(request.POST, request.FILES)
		if c_form.is_valid():
			Name 		= request.POST.get('Name','')
			Email 		= request.POST.get('Email','')
			Contact		= request.POST.get('Contact','')
			Message 	= request.POST.get('Message','')
			Files 		= request.FILES.getlist('File')
			Now 		= datetime.now()
			Date 		= Now.strftime('%Y')+'_'+Now.strftime('%d')+'_'+Now.strftime('%b')+'_'+Now.strftime('%I')+\
												'_'+Now.strftime('%M')+'_'+Now.strftime('%S')+'_'+Now.strftime('%p')
			File_status = len(Files) if len(Files)!=0 else 0

			if File_status == 0:
				form_obj = models.Contact_form_model(Name = Name, Email = Email, Contact = Contact,
													Message = Message, Date = Date, File_status = File_status)
				form_obj.save()
			else:
				form_obj = models.Contact_form_model(Name = Name, Email = Email, Contact = Contact,
													Message = Message, Date = Date, File_status = File_status)
				form_obj.save()

				U_id = models.Contact_form_model.objects.get(Date = Date).U_id
				for data in Files:
					file_obj = models.File_model.objects.create(U_id = U_id, File=data)
					file_obj.save()

			messages.add_message(request, messages.INFO, "Thank You.. {}".format(Name))
			send_whatsapp_message(Name,Email,Contact,Message,File_status)
			return redirect('/')
		else:
			messages.add_message(request, messages.INFO, 'Thank You for Giving your Precious Time.')
			return redirect('/')


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def send_whatsapp_message(Name,Email,Contact,Message,File_status):
	account_sid = 'ACfa44115d0ff5f4602437ca7a4130b110'
	auth_token = 'ed2ff6c9068fc1ae3a3e3fff11026de0'
	client = Client(account_sid, auth_token)

	message = client.messages.create(
	                     body="Hello Pratik,\n\nSomeone trying to contact you.\n\nName: {}\nContact: {}\nEmail: {}\nFile_status: {}\n\nMessage: {}".format(Name,Contact,Email,File_status,Message),
	                     from_='whatsapp:+14155238886',
	                     to='whatsapp:+917000681073'
	                 )
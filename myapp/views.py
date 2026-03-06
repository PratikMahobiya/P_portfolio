import os
import requests
from datetime import datetime
from django.conf import settings
from django.http import Http404
from django.contrib import messages
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import SuspiciousFileOperation
from django.utils._os import safe_join

from . import forms
from . import models

def Index(request):
	# messages.add_message(request, messages.INFO, "Thank You.. ")
	return render(request, "index.html")

def Contact(request):
    if request.method == 'POST':
        c_form = forms.Contact_Form(request.POST, request.FILES)
        
        if c_form.is_valid():
            # 1. Use cleaned_data for sanitized input
            name = c_form.cleaned_data.get('Name')
            email = c_form.cleaned_data.get('Email')
            contact = c_form.cleaned_data.get('Contact')
            message = c_form.cleaned_data.get('Message')
            files = request.FILES.getlist('File')
            file_status = len(files)
            
            date_str = datetime.now().strftime('%Y_%d_%b_%I_%M_%S_%p')

            # 2. Save the object ONCE
            form_obj = models.Contact_form_model.objects.create(
                Name=name, 
                Email=email, 
                Contact=contact,
                Message=message, 
                Date=date_str, 
                File_status=file_status
            )

            # 3. Use the newly created object's ID directly (No need to re-query the DB)
            if file_status > 0:
                # Assuming U_id is an integer field or ForeignKey. 
                # If it's a ForeignKey, it's better to pass the object: form_obj
                for data in files:
                    models.File_model.objects.create(U_id=form_obj.pk, File=data)

            messages.success(request, f"Thank You, {name}. I will get back to you soon.")
            return redirect('/')
        else:
            messages.warning(request, 'Please correct the errors in the form.')
            # Ideally, re-render the template with form errors here instead of redirecting
            return redirect('/') 


def download(request, path):
    # 4. Use safe_join to prevent directory traversal attacks
    try:
        file_path = safe_join(settings.MEDIA_ROOT, path)
    except SuspiciousFileOperation:
        raise Http404("Invalid file path")

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
            return response
    raise Http404


@receiver(post_save, sender=models.Contact_form_model)
def send_sms(sender, instance, created, **kwargs):
    if created and instance.Contact != 0:
        
        # Note: In a true microservices/optimized architecture, 
        # this logic should be sent to a Celery task or an SQS queue 
        # to prevent blocking the HTTP response.
        
        url = "https://www.fast2sms.com/dev/bulkV2"
        
        # 5. Pass parameters as a dictionary to let requests handle URL encoding safely
        payload = {
            "message": f"Hello Pratik,\nSomeone trying to contact you.\nName: {instance.Name}\nContact: {instance.Contact}\nEmail: {instance.Email}\n\nMessage: {instance.Message}",
            "language": "english",
            "route": "q",
            "numbers": "7000681073",
            "flash": "1"
        }
        
        headers = {
            'authorization': "6a0iXHGODBECvnVbmSoeYPd5K1Mgl3thUL2zNQp79cJWRfTZFx40eYPvV2SJ1lKXU9Tzp8qGtCsDcuL5",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }

        try:
            # Set a timeout so your web server doesn't hang indefinitely if the API goes down
            requests.post(url, data=payload, headers=headers, timeout=5)
        except requests.exceptions.RequestException as e:
            # Log the error here instead of crashing the user's request
            print(f"Failed to send SMS: {e}")
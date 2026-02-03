# yourapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


def send_appointment_email( name, email, invoice, phone=None, message=None):
    print ('celery added')
    subject = 'New Order '
    email_message = f"""
    New order booked with the following details:
    Name : {name}
    Email : {email}
    invoice : {invoice}
    """
    try:
        send_mail(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            ['anirbansingha1@outlook.com','bwe58611@gmail.com','camc4283@gmail.com'],
            fail_silently=False,
        )
    except Exception as e:
        # Log the error somewhere
        print ('Fail send email '+str(e))
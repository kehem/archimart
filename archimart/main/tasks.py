# yourapp/tasks.py
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_appointment_email(name, email, invoice, phone=None, message=None, items=None, total=None, tracking_link=None, order_date=None):
    """Send order confirmation as HTML email rendered from `dashboard/mail.html`.

    Keeps original parameters for compatibility and adds optional context
    values for richer templates (items, total, tracking_link, order_date).
    """
    print('celery added')
    subject = 'Order Confirmation - Archimart'

    # Build template context
    context = {
        'customer_name': name,
        'customer_email': email,
        'invoice': invoice,
        'phone': phone,
        'message': message,
        'items': items or [],
        'total': total or '',
        'tracking_link': tracking_link or '#',
        'date': order_date or '',
    }

    try:
        # Render HTML from the template located at `main/templates/dashboard/mail.html`
        html_content = render_to_string('dashboard/mail.html', context)

        # Fallback plain-text version
        text_content = strip_tags(html_content)

        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER)

        # recipients: send to customer and BCC site admins (previous hard-coded addresses)
        to_emails = ['anirbansingha1@outlook.com', 'bwe58611@gmail.com', 'camc4283@gmail.com']
        # bcc_admins = ['anirbansingha1@outlook.com', 'bwe58611@gmail.com', 'camc4283@gmail.com']

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.attach_alternative(html_content, 'text/html')
        msg.send(fail_silently=False)

    except Exception as e:
        # Log the error somewhere appropriate; for now print to console
        print('Fail send email ' + str(e))
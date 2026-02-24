# yourapp/tasks.py
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


@shared_task(
    bind=True, 
    max_retries=3, 
    default_retry_delay=10  # Retry after 10 second if it fails
)
def send_appointment_email(self, name, email, invoice, phone=None, message=None, items=None, total=None, tracking_link=None, order_date=None):
    """Send order confirmation as HTML email rendered from `dashboard/mail.html`.

    Keeps original parameters for compatibility and adds optional context
    values for richer templates (items, total, tracking_link, order_date).
    """
    logger.info(f"Starting to send confirmation email for invoice {invoice} to {email}")
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
        html_content = render_to_string('dashboard/mail.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject='Order Confirmation - Archimart',
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            bcc=['bwe58611@gmail.com', 'camc4283@gmail.com', 'anirbansingha1@outlook.com']
        )
        msg.attach_alternative(html_content, 'text/html')
        
        return msg.send(fail_silently=False)

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        # This will trigger the retry logic defined in the decorator
        raise self.retry(exc=e)
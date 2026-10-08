from django.core.mail import send_mail
from celery import shared_task
from config.settings import EMAIL_DEFAULT_FROM
import logging

logger = logging.getLogger(__name__)


@shared_task()
def send_email_task(subject, message, email_address):
    """Sends email"""
    try:
        result = send_mail(
            subject,
            f"\t{message}\n",
            EMAIL_DEFAULT_FROM, 
            [email_address],
            fail_silently=False,
        )
        if result == 1:
            logger.info(f"Email successfully sent to: {email_address}")
        else:
            logger.warning(f"Email send returned unexpected result: {result} to {email_address}")
    except Exception as e:
        logging.error(f"Error sending email to {email_address}: {type(e).__name__}: {e}")
        

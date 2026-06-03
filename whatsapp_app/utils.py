"""
Utility functions for WhatsApp message sending and processing
"""

import logging
import time
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from .models import BulkMessage, MessageLog, Contact
from .whatsapp_sender import WhatsAppSender

logger = logging.getLogger(__name__)


def send_bulk_messages_async(message_id, target_language='en'):
    """
    Send bulk messages for a specific BulkMessage instance
    Can be called from Celery task or directly
    
    Args:
        message_id: ID of BulkMessage to send
        target_language: 'en', 'te', or 'both'
    """
    try:
        message = BulkMessage.objects.get(id=message_id)
        
        # Get contacts based on language
        if target_language == 'both':
            contacts = Contact.objects.filter(
                school=message.school,
                is_blocked=False
            )
        else:
            contacts = Contact.objects.filter(
                school=message.school,
                language=target_language,
                is_blocked=False
            )
        
        # Get the message content for this language
        if target_language == 'te' and message.message_te:
            message_content = message.message_te
        else:
            message_content = message.message_en
        
        # Prepare contact list
        contact_list = [
            {'name': c.name, 'phone': c.phone}
            for c in contacts
        ]
        
        if not contact_list:
            logger.warning(f"No contacts found for message {message_id}")
            message.status = 'failed'
            message.save()
            return False
        
        # Initialize WhatsApp sender with ChromeDriver path from settings
        chrome_driver_path = getattr(settings, 'CHROME_DRIVER_PATH', 'chromedriver.exe')
        sender = WhatsAppSender(chrome_driver_path=chrome_driver_path)
        
        if not sender.setup_driver():
            logger.error(f"Failed to setup WebDriver for message {message_id}")
            message.status = 'failed'
            message.save()
            return False
        
        if not sender.open_whatsapp_web():
            logger.error(f"Failed to open WhatsApp Web for message {message_id}")
            sender.close()
            message.status = 'failed'
            message.save()
            return False
        
        # Define progress callback
        def progress_callback(current, total, status):
            with transaction.atomic():
                if status == 'sent':
                    message.sent_count = current
                elif status == 'failed':
                    message.failed_count += 1
                
                message.save()
                logger.info(f"Progress: {current}/{total} - {status}")
        
        # Send messages
        results = sender.send_bulk_message(
            contact_list,
            message_content,
            progress_callback=progress_callback
        )
        
        # Update message logs
        with transaction.atomic():
            for contact_data in results['sent']:
                MessageLog.objects.filter(
                    bulk_message=message,
                    contact__phone=contact_data['phone']
                ).update(
                    status='sent',
                    sent_at=timezone.now(),
                    attempt_count=1
                )
            
            for contact_data in results['failed']:
                MessageLog.objects.filter(
                    bulk_message=message,
                    contact__phone=contact_data['phone']
                ).update(
                    status='failed',
                    error_message='Failed to send',
                    attempt_count=1
                )
        
        # Update message status
        message.status = 'completed'
        message.completed_at = timezone.now()
        message.sent_count = len(results['sent'])
        message.failed_count = len(results['failed'])
        message.save()
        
        sender.close()
        
        logger.info(f"Message {message_id} completed. Sent: {len(results['sent'])}, Failed: {len(results['failed'])}")
        return True
        
    except BulkMessage.DoesNotExist:
        logger.error(f"Message with ID {message_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending bulk message {message_id}: {str(e)}")
        try:
            message = BulkMessage.objects.get(id=message_id)
            message.status = 'failed'
            message.save()
        except:
            pass
        return False


def retry_failed_messages(message_id, max_retries=3):
    """
    Retry sending failed messages
    
    Args:
        message_id: ID of BulkMessage
        max_retries: Maximum retry attempts
    """
    try:
        message = BulkMessage.objects.get(id=message_id)
        
        # Get failed logs
        failed_logs = MessageLog.objects.filter(
            bulk_message=message,
            status='failed',
            attempt_count__lt=max_retries
        )
        
        if not failed_logs.exists():
            logger.info(f"No failed messages to retry for message {message_id}")
            return True
        
        # Get contacts for failed logs
        failed_contacts = [
            {
                'name': log.contact.name,
                'phone': log.contact.phone,
                'log_id': log.id
            }
            for log in failed_logs
        ]
        
        # Initialize WhatsApp sender
        sender = WhatsAppSender()
        
        if not sender.setup_driver():
            logger.error(f"Failed to setup WebDriver for retry")
            return False
        
        if not sender.open_whatsapp_web():
            logger.error(f"Failed to open WhatsApp Web for retry")
            sender.close()
            return False
        
        # Get message content
        message_content = message.message_en or message.message_te
        
        # Send to failed contacts
        sent_count = 0
        for contact_data in failed_contacts:
            try:
                if sender.search_and_open_contact(contact_data['phone']):
                    if sender.send_message(message_content):
                        MessageLog.objects.filter(id=contact_data['log_id']).update(
                            status='sent',
                            sent_at=timezone.now(),
                            attempt_count=1
                        )
                        sent_count += 1
                    else:
                        MessageLog.objects.filter(id=contact_data['log_id']).update(
                            attempt_count=1
                        )
                    time.sleep(2)  # Delay between messages
            except Exception as e:
                logger.error(f"Error retrying message for {contact_data['phone']}: {str(e)}")
        
        sender.close()
        
        logger.info(f"Retry completed. {sent_count} messages sent")
        return True
        
    except BulkMessage.DoesNotExist:
        logger.error(f"Message with ID {message_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error during retry: {str(e)}")
        return False


def get_message_statistics(message_id):
    """
    Get detailed statistics for a message
    
    Args:
        message_id: ID of BulkMessage
        
    Returns:
        Dictionary with statistics
    """
    try:
        message = BulkMessage.objects.get(id=message_id)
        
        logs = MessageLog.objects.filter(bulk_message=message)
        
        stats = {
            'total': message.total_contacts,
            'sent': logs.filter(status='sent').count(),
            'failed': logs.filter(status='failed').count(),
            'pending': logs.filter(status='pending').count(),
            'blocked': logs.filter(status='blocked').count(),
            'success_rate': 0,
            'failure_rate': 0,
            'avg_time': 0,
        }
        
        if stats['total'] > 0:
            stats['success_rate'] = (stats['sent'] / stats['total']) * 100
            stats['failure_rate'] = (stats['failed'] / stats['total']) * 100
        
        # Calculate average sending time
        sent_logs = logs.filter(status='sent').exclude(sent_at__isnull=True)
        if sent_logs.exists():
            time_diffs = [
                (log.sent_at - log.created_at).total_seconds()
                for log in sent_logs if log.sent_at
            ]
            if time_diffs:
                stats['avg_time'] = sum(time_diffs) / len(time_diffs)
        
        return stats
        
    except BulkMessage.DoesNotExist:
        return None
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return None


def validate_phone_number(phone):
    """
    Validate phone number format
    
    Args:
        phone: Phone number string
        
    Returns:
        Tuple (is_valid, cleaned_phone)
    """
    # Remove non-digits
    cleaned = ''.join(filter(str.isdigit, phone))
    
    # Check length (10-15 digits)
    if len(cleaned) < 10 or len(cleaned) > 15:
        return False, None
    
    return True, cleaned

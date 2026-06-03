"""
Views for the WhatsApp notification system
"""

import logging
import json
import csv
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Contact, BulkMessage, MessageLog, ActivityLog, 
    SchoolSetting, HolidayTemplate
)
from .forms import (
    ContactUploadForm, BulkMessageForm, HolidayTemplateForm,
    ContactSearchForm, ExcelHelper, DirectMessageForm
)
from .whatsapp_sender import WhatsAppSender

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_activity(user, action, description, request):
    """Log user activity"""
    ActivityLog.objects.create(
        admin_user=user,
        action=action,
        description=description,
        ip_address=get_client_ip(request)
    )


def send_messages_to_numbers(message_obj, phone_numbers, message_text):
    """
    Send WhatsApp messages to specific numbers
    
    Args:
        message_obj: BulkMessage instance
        phone_numbers: List of phone numbers (with country code)
        message_text: Message text to send
        
    Returns:
        Tuple (success: bool, sent_count: int, failed_count: int)
    """
    try:
        sender = WhatsAppSender()
        
        if not sender.setup_driver():
            logger.error("Failed to setup WhatsApp driver")
            return False, 0, len(phone_numbers)
        
        if not sender.open_whatsapp_web():
            logger.error("Failed to open WhatsApp Web - may need QR scan")
            sender.close()
            return False, 0, len(phone_numbers)
        
        sent_count = 0
        failed_count = 0
        
        # Get or create message logs
        message_logs = MessageLog.objects.filter(
            bulk_message=message_obj,
            status='pending'
        )
        
        for log in message_logs:
            try:
                phone = log.contact.phone
                logger.info(f"Sending message to {phone}")
                
                # Search and open contact
                if sender.search_and_open_contact(phone):
                    # Send message
                    if sender.send_message(message_text):
                        # Update log as sent
                        log.status = 'sent'
                        log.sent_at = timezone.now()
                        log.save()
                        sent_count += 1
                        logger.info(f"Message sent successfully to {phone}")
                    else:
                        log.status = 'failed'
                        log.error_message = 'Failed to send message'
                        log.save()
                        failed_count += 1
                else:
                    log.status = 'failed'
                    log.error_message = 'Contact not found'
                    log.save()
                    failed_count += 1
                    
            except Exception as e:
                logger.error(f"Error sending to {log.contact.phone}: {str(e)}")
                log.status = 'failed'
                log.error_message = str(e)
                log.save()
                failed_count += 1
        
        sender.close()
        
        # Update message status
        if failed_count == 0:
            message_obj.status = 'completed'
        elif sent_count > 0:
            message_obj.status = 'partial'
        else:
            message_obj.status = 'failed'
        message_obj.sent_count = sent_count
        message_obj.completed_at = timezone.now()
        message_obj.save()
        
        return True, sent_count, failed_count
        
    except Exception as e:
        logger.error(f"Error in send_messages_to_numbers: {str(e)}")
        return False, 0, len(phone_numbers)



# ============= Authentication Views =============

def login_view(request):
    """Admin login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            log_activity(user, 'login', f'Admin login from {get_client_ip(request)}', request)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })
    
    return render(request, 'login.html')


@login_required(login_url='login')
def logout_view(request):
    """Admin logout"""
    user = request.user
    log_activity(user, 'logout', 'Admin logout', request)
    logout(request)
    return redirect('login')


# ============= Dashboard Views =============

@login_required(login_url='login')
def dashboard(request):
    """Main dashboard with statistics"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        # Create school setting if doesn't exist
        school = SchoolSetting.objects.create(
            school_name='My School',
            admin_user=request.user
        )
    
    # Get statistics
    total_contacts = Contact.objects.filter(school=school).count()
    total_messages = BulkMessage.objects.filter(school=school).count()
    sent_messages = BulkMessage.objects.filter(
        school=school, 
        status='completed'
    ).aggregate(Count('sent_count'))['sent_count__count'] or 0
    
    pending_messages = BulkMessage.objects.filter(
        school=school,
        status__in=['draft', 'scheduled', 'sending']
    ).count()
    
    recent_messages = BulkMessage.objects.filter(
        school=school
    ).order_by('-created_at')[:10]
    
    context = {
        'school': school,
        'total_contacts': total_contacts,
        'total_messages': total_messages,
        'sent_messages': sent_messages,
        'pending_messages': pending_messages,
        'recent_messages': recent_messages,
    }
    
    return render(request, 'dashboard.html', context)


# ============= Contact Management Views =============

@login_required(login_url='login')
def contacts_list(request):
    """List all contacts with search and filter"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return redirect('dashboard')
    
    contacts = Contact.objects.filter(school=school)
    
    # Search and filter
    form = ContactSearchForm(request.GET)
    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        language = form.cleaned_data.get('language')
        is_blocked = form.cleaned_data.get('is_blocked')
        
        if search_query:
            contacts = contacts.filter(
                Q(name__icontains=search_query) |
                Q(phone__icontains=search_query)
            )
        
        if language:
            contacts = contacts.filter(language=language)
        
        if is_blocked is not None:
            contacts = contacts.filter(is_blocked=is_blocked)
    
    # Pagination
    paginator = Paginator(contacts, 20)
    page_number = request.GET.get('page')
    contacts_page = paginator.get_page(page_number)
    
    context = {
        'contacts': contacts_page,
        'form': form,
        'school': school,
        'total_count': contacts.count(),
    }
    
    return render(request, 'contacts_list.html', context)


@login_required(login_url='login')
def upload_contacts(request):
    """Upload contacts from Excel file"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ContactUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            language = form.cleaned_data['language']
            overwrite = form.cleaned_data['overwrite']
            
            success, message, stats = ExcelHelper.import_contacts(
                excel_file, school, language, overwrite
            )
            
            if success:
                log_activity(
                    request.user, 'upload',
                    f"Imported {stats['imported']} contacts",
                    request
                )
                context = {
                    'success': True,
                    'message': message,
                    'stats': stats,
                    'form': form,
                    'school': school,
                }
            else:
                context = {
                    'success': False,
                    'message': message,
                    'form': form,
                    'school': school,
                }
            
            return render(request, 'upload_contacts.html', context)
    else:
        form = ContactUploadForm()
    
    context = {
        'form': form,
        'school': school,
    }
    
    return render(request, 'upload_contacts.html', context)


@login_required(login_url='login')
def delete_contacts(request, contact_id=None):
    """Delete individual or bulk contacts"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return redirect('dashboard')
    
    if request.method == 'POST':
        if contact_id:
            contact = get_object_or_404(Contact, id=contact_id, school=school)
            contact.delete()
            log_activity(request.user, 'delete', f'Deleted contact: {contact.name}', request)
            return redirect('contacts_list')
        else:
            contact_ids = request.POST.getlist('contact_ids')
            Contact.objects.filter(id__in=contact_ids, school=school).delete()
            log_activity(request.user, 'delete', f'Deleted {len(contact_ids)} contacts', request)
            return redirect('contacts_list')
    
    return redirect('contacts_list')


# ============= Message Management Views =============

@login_required(login_url='login')
def messages_list(request):
    """List all bulk messages"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return redirect('dashboard')
    
    messages = BulkMessage.objects.filter(school=school).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)
    
    context = {
        'messages': messages_page,
        'school': school,
    }
    
    return render(request, 'messages_list.html', context)


@login_required(login_url='login')
def create_message(request):
    """Create and schedule a bulk message"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BulkMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.school = school
            message.created_by = request.user
            message.save()
            
            log_activity(
                request.user, 'send',
                f'Created message: {message.title}',
                request
            )
            
            return redirect('message_detail', message_id=message.id)
    else:
        form = BulkMessageForm()
    
    context = {
        'form': form,
        'school': school,
        'templates': HolidayTemplate.objects.filter(school=school),
    }
    
    return render(request, 'create_message.html', context)


@login_required(login_url='login')
def message_detail(request, message_id):
    """View message details and sending logs"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return redirect('dashboard')
    
    message = get_object_or_404(BulkMessage, id=message_id, school=school)
    
    logs = MessageLog.objects.filter(bulk_message=message).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    logs_page = paginator.get_page(page_number)
    
    context = {
        'message': message,
        'logs': logs_page,
        'school': school,
    }
    
    return render(request, 'message_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def send_message(request, message_id):
    """Start sending bulk message"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return JsonResponse({'error': 'School not found'}, status=400)
    
    message = get_object_or_404(BulkMessage, id=message_id, school=school)
    
    if message.status not in ['draft', 'completed', 'failed']:
        return JsonResponse({
            'error': 'Message is already being sent or scheduled'
        }, status=400)
    
    target_language = request.POST.get('target_language', 'en')
    
    # Get contacts to send to
    if target_language == 'both':
        contacts = Contact.objects.filter(school=school, is_blocked=False)
    else:
        contacts = Contact.objects.filter(
            school=school,
            language=target_language,
            is_blocked=False
        )
    
    # Create message logs
    message.total_contacts = contacts.count()
    message.status = 'sending'
    message.started_at = timezone.now()
    message.save()
    
    for contact in contacts:
        MessageLog.objects.get_or_create(
            bulk_message=message,
            contact=contact,
            defaults={'status': 'pending'}
        )
    
    log_activity(
        request.user, 'send',
        f'Started sending message: {message.title} to {message.total_contacts} contacts',
        request
    )
    
    return JsonResponse({
        'success': True,
        'message_id': message.id,
        'total_contacts': message.total_contacts
    })


@login_required(login_url='login')
def export_report(request, message_id):
    """Export message sending report as CSV"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return JsonResponse({'error': 'School not found'}, status=400)
    
    message = get_object_or_404(BulkMessage, id=message_id, school=school)
    
    logs = MessageLog.objects.filter(bulk_message=message)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="report_{message.id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Contact Name', 'Phone', 'Status', 'Sent At', 'Error'])
    
    for log in logs:
        writer.writerow([
            log.contact.name,
            log.contact.phone,
            log.get_status_display(),
            log.sent_at or '',
            log.error_message or ''
        ])
    
    log_activity(
        request.user, 'export',
        f'Exported report for message: {message.title}',
        request
    )
    
    return response


# ============= Direct Message Sending Views =============

@login_required(login_url='login')
def send_direct_message(request):
    """Send message directly to specific numbers (single, multiple, or file)"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DirectMessageForm(request.POST, request.FILES)
        if form.is_valid():
            sending_mode = form.cleaned_data['sending_mode']
            message_en = form.cleaned_data['message_en']
            message_te = form.cleaned_data['message_te']
            title = form.cleaned_data['title']
            
            # Parse phone numbers based on mode
            phone_numbers = []
            
            try:
                if sending_mode == 'single':
                    phone_numbers = [form.cleaned_data['phone_number']]
                
                elif sending_mode == 'multiple':
                    numbers_text = form.cleaned_data['phone_numbers']
                    # Split by comma or newline
                    phone_numbers = [
                        n.strip() for n in numbers_text.replace(',', '\n').split('\n')
                        if n.strip() and n.strip().isdigit()
                    ]
                
                elif sending_mode == 'file':
                    phone_file = request.FILES['phone_file']
                    success, result = ExcelHelper.validate_and_parse_excel(phone_file)
                    if not success:
                        return render(request, 'send_direct_message.html', {
                            'form': form,
                            'error': result,
                            'school': school,
                        })
                    # Extract phone numbers from parsed data
                    phone_numbers = [contact['phone'] for contact in result]
                
                if not phone_numbers:
                    return render(request, 'send_direct_message.html', {
                        'form': form,
                        'error': 'No valid phone numbers found',
                        'school': school,
                    })
                
                # Create a BulkMessage for tracking
                message = BulkMessage.objects.create(
                    school=school,
                    title=title,
                    message_en=message_en,
                    message_te=message_te,
                    created_by=request.user,
                    total_contacts=len(phone_numbers),
                    status='sending',
                    started_at=timezone.now()
                )
                
                # Create temporary contacts and message logs
                created_logs = []
                for phone in phone_numbers:
                    # Create or get a temporary contact
                    contact, created = Contact.objects.get_or_create(
                        phone=phone,
                        school=school,
                        defaults={
                            'name': f'Direct Send {phone}',
                            'language': 'en'
                        }
                    )
                    
                    # Create message log
                    msg_log = MessageLog.objects.create(
                        bulk_message=message,
                        contact=contact,
                        status='pending'
                    )
                    created_logs.append(msg_log)
                
                log_activity(
                    request.user, 'send_direct',
                    f'Sent direct message to {len(phone_numbers)} numbers: {title}',
                    request
                )
                
                # Actually send the messages via WhatsApp
                send_success, sent_count, failed_count = send_messages_to_numbers(
                    message, 
                    phone_numbers, 
                    message_en  # Send English message by default
                )
                
                return render(request, 'send_direct_message.html', {
                    'success': True,
                    'message': message,
                    'phone_count': len(phone_numbers),
                    'sent_count': sent_count,
                    'failed_count': failed_count,
                    'send_success': send_success,
                    'school': school,
                })
            
            except Exception as e:
                logger.error(f"Error in direct message sending: {str(e)}")
                return render(request, 'send_direct_message.html', {
                    'form': form,
                    'error': f'Error processing: {str(e)}',
                    'school': school,
                })
    else:
        form = DirectMessageForm()
    
    context = {
        'form': form,
        'school': school,
    }
    
    return render(request, 'send_direct_message.html', context)


# ============= Holiday Templates Views =============

@login_required(login_url='login')
def templates_list(request):
    """List holiday templates"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return redirect('dashboard')
    
    templates = HolidayTemplate.objects.filter(school=school)
    
    context = {
        'templates': templates,
        'school': school,
    }
    
    return render(request, 'templates_list.html', context)


@login_required(login_url='login')
def create_template(request):
    """Create new holiday template"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = HolidayTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.school = school
            template.save()
            return redirect('templates_list')
    else:
        form = HolidayTemplateForm()
    
    context = {
        'form': form,
        'school': school,
    }
    
    return render(request, 'create_template.html', context)


# ============= API Views =============

@login_required(login_url='login')
@require_http_methods(["GET"])
def api_message_progress(request, message_id):
    """API endpoint for message sending progress"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return JsonResponse({'error': 'School not found'}, status=400)
    
    message = get_object_or_404(BulkMessage, id=message_id, school=school)
    
    sent = MessageLog.objects.filter(
        bulk_message=message,
        status='sent'
    ).count()
    
    failed = MessageLog.objects.filter(
        bulk_message=message,
        status='failed'
    ).count()
    
    pending = message.total_contacts - sent - failed
    
    progress_percent = 0
    if message.total_contacts > 0:
        progress_percent = int((sent + failed) / message.total_contacts * 100)
    
    return JsonResponse({
        'total': message.total_contacts,
        'sent': sent,
        'failed': failed,
        'pending': pending,
        'progress': progress_percent,
        'status': message.status,
    })


@login_required(login_url='login')
@require_http_methods(["GET"])
def api_contacts_stats(request):
    """API endpoint for contacts statistics"""
    try:
        school = SchoolSetting.objects.get(admin_user=request.user)
    except SchoolSetting.DoesNotExist:
        return JsonResponse({'error': 'School not found'}, status=400)
    
    total = Contact.objects.filter(school=school).count()
    english = Contact.objects.filter(school=school, language='en').count()
    telugu = Contact.objects.filter(school=school, language='te').count()
    blocked = Contact.objects.filter(school=school, is_blocked=True).count()
    
    return JsonResponse({
        'total': total,
        'english': english,
        'telugu': telugu,
        'blocked': blocked,
        'active': total - blocked,
    })

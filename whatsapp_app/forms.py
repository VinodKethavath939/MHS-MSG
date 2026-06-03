"""
Django forms for the WhatsApp notification system
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Contact, BulkMessage, HolidayTemplate
import pandas as pd


class ContactUploadForm(forms.Form):
    """Form for uploading Excel file with contacts"""
    
    excel_file = forms.FileField(
        label='Upload Excel File (*.xlsx, *.xls, *.csv)',
        help_text='Excel file must have "Name" and "Phone" columns'
    )
    language = forms.ChoiceField(
        choices=[('en', 'English'), ('te', 'Telugu')],
        label='Default Language for Contacts'
    )
    overwrite = forms.BooleanField(
        required=False,
        label='Overwrite existing contacts with same phone number'
    )
    
    def clean_excel_file(self):
        file = self.cleaned_data['excel_file']
        
        # Check file extension
        valid_extensions = ['.xlsx', '.xls', '.csv']
        file_ext = file.name.split('.')[-1].lower()
        
        if f'.{file_ext}' not in valid_extensions:
            raise ValidationError(
                'Invalid file format. Please upload .xlsx, .xls, or .csv file'
            )
        
        # Check file size (max 5MB)
        if file.size > 5 * 1024 * 1024:
            raise ValidationError('File size must not exceed 5MB')
        
        return file


class BulkMessageForm(forms.ModelForm):
    """Form for creating and sending bulk messages"""
    
    target_language = forms.ChoiceField(
        choices=[('en', 'English'), ('te', 'Telugu'), ('both', 'Both')],
        label='Send to contacts with language',
        initial='en'
    )
    
    class Meta:
        model = BulkMessage
        fields = ['title', 'message_en', 'message_te', 'scheduled_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Message Title',
                'maxlength': '255'
            }),
            'message_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Type your message in English...'
            }),
            'message_te': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Type your message in Telugu (Optional)...'
            }),
            'scheduled_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        message_en = cleaned_data.get('message_en')
        message_te = cleaned_data.get('message_te')
        
        if not message_en and not message_te:
            raise ValidationError('Please provide message in at least one language')
        
        if message_en and len(message_en) > 4096:
            raise ValidationError('English message is too long (max 4096 characters)')
        
        if message_te and len(message_te) > 4096:
            raise ValidationError('Telugu message is too long (max 4096 characters)')
        
        return cleaned_data


class HolidayTemplateForm(forms.ModelForm):
    """Form for holiday notice templates"""
    
    class Meta:
        model = HolidayTemplate
        fields = ['name', 'message_en', 'message_te']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Template Name',
                'maxlength': '255'
            }),
            'message_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Holiday notice in English...'
            }),
            'message_te': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Holiday notice in Telugu (Optional)...'
            }),
        }


class ContactSearchForm(forms.Form):
    """Form for searching and filtering contacts"""
    
    search = forms.CharField(
        required=False,
        label='Search by name or phone',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search contacts...'
        })
    )
    language = forms.ChoiceField(
        required=False,
        choices=[('', 'All Languages'), ('en', 'English'), ('te', 'Telugu')],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    is_blocked = forms.NullBooleanField(
        required=False,
        label='Show blocked contacts only',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class ExcelHelper:
    """Helper class to process Excel files"""
    
    REQUIRED_COLUMNS = ['name', 'phone']
    
    @staticmethod
    def validate_and_parse_excel(file_obj):
        """
        Validate and parse Excel file
        
        Args:
            file_obj: Uploaded file object
            
        Returns:
            Tuple (success: bool, data: list or error: str)
        """
        try:
            # Read Excel file
            if file_obj.name.endswith('.csv'):
                df = pd.read_csv(file_obj)
            else:
                df = pd.read_excel(file_obj)
            
            # Normalize column names to lowercase
            df.columns = df.columns.str.lower().str.strip()
            
            # Check required columns
            if not all(col in df.columns for col in ExcelHelper.REQUIRED_COLUMNS):
                missing = [col for col in ExcelHelper.REQUIRED_COLUMNS if col not in df.columns]
                return False, f"Missing required columns: {', '.join(missing)}"
            
            # Clean and validate data
            contacts = []
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    name = str(row['name']).strip()
                    phone = str(row['phone']).strip()
                    
                    # Validate phone number (remove non-digits)
                    phone_clean = ''.join(filter(str.isdigit, phone))
                    
                    if not phone_clean or len(phone_clean) < 10:
                        errors.append(f"Row {idx + 2}: Invalid phone number")
                        continue
                    
                    if not name or len(name) < 2:
                        errors.append(f"Row {idx + 2}: Invalid name")
                        continue
                    
                    contacts.append({
                        'name': name,
                        'phone': phone_clean
                    })
                except Exception as e:
                    errors.append(f"Row {idx + 2}: {str(e)}")
            
            if errors:
                error_msg = '\n'.join(errors[:10])
                if len(errors) > 10:
                    error_msg += f"\n... and {len(errors) - 10} more errors"
                return False, f"Validation errors:\n{error_msg}"
            
            if not contacts:
                return False, "No valid contacts found in file"
            
            return True, contacts
            
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
    
    @staticmethod
    def import_contacts(file_obj, school, language='en', overwrite=False):
        """
        Import contacts from Excel file to database
        
        Args:
            file_obj: Uploaded file object
            school: SchoolSetting instance
            language: Default language for contacts
            overwrite: Whether to overwrite existing contacts
            
        Returns:
            Tuple (success: bool, message: str, stats: dict)
        """
        success, result = ExcelHelper.validate_and_parse_excel(file_obj)
        
        if not success:
            return False, result, {}
        
        contacts_data = result
        
        try:
            imported = 0
            updated = 0
            skipped = 0
            
            for contact_data in contacts_data:
                phone = contact_data['phone']
                
                try:
                    existing = Contact.objects.filter(
                        phone=phone,
                        school=school
                    ).first()
                    
                    if existing:
                        if overwrite:
                            existing.name = contact_data['name']
                            existing.language = language
                            existing.save()
                            updated += 1
                        else:
                            skipped += 1
                    else:
                        Contact.objects.create(
                            name=contact_data['name'],
                            phone=phone,
                            language=language,
                            school=school
                        )
                        imported += 1
                except Exception as e:
                    logger.error(f"Error importing contact {phone}: {str(e)}")
                    skipped += 1
            
            message = f"Import successful! Imported: {imported}, Updated: {updated}, Skipped: {skipped}"
            stats = {
                'imported': imported,
                'updated': updated,
                'skipped': skipped,
                'total': len(contacts_data)
            }
            
            return True, message, stats
            
        except Exception as e:
            return False, f"Error importing contacts: {str(e)}", {}


import logging
logger = logging.getLogger(__name__)


class DirectMessageForm(forms.Form):
    """Form for sending messages directly to numbers (single, multiple, or file)"""
    
    SENDING_MODE_CHOICES = [
        ('single', 'Single Number'),
        ('multiple', 'Multiple Numbers'),
        ('file', 'Upload File'),
    ]
    
    sending_mode = forms.ChoiceField(
        choices=SENDING_MODE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        }),
        initial='single',
        label='Choose sending mode'
    )
    
    # Single number field
    phone_number = forms.CharField(
        required=False,
        label='Phone Number',
        help_text='Enter phone number with country code (e.g., 919876543210)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '919876543210',
            'maxlength': '20'
        })
    )
    
    # Multiple numbers field
    phone_numbers = forms.CharField(
        required=False,
        label='Phone Numbers',
        help_text='Enter multiple numbers separated by commas or new lines',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': '919876543210\n919876543211\n919876543212'
        })
    )
    
    # File upload
    phone_file = forms.FileField(
        required=False,
        label='Upload File',
        help_text='Upload Excel (.xlsx, .xls) or CSV file with phone numbers in first column',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls,.csv'
        })
    )
    
    # Message fields
    title = forms.CharField(
        label='Message Title',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Message Title',
        })
    )
    
    message_en = forms.CharField(
        label='Message (English)',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Type your message in English...'
        })
    )
    
    message_te = forms.CharField(
        required=False,
        label='Message (Telugu)',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Type your message in Telugu (Optional)...'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        sending_mode = cleaned_data.get('sending_mode')
        phone_number = cleaned_data.get('phone_number', '').strip()
        phone_numbers = cleaned_data.get('phone_numbers', '').strip()
        phone_file = cleaned_data.get('phone_file')
        
        message_en = cleaned_data.get('message_en', '').strip()
        message_te = cleaned_data.get('message_te', '').strip()
        
        # Validate messages
        if not message_en and not message_te:
            raise ValidationError('Please provide message in at least one language')
        
        if message_en and len(message_en) > 4096:
            raise ValidationError('English message is too long (max 4096 characters)')
        
        if message_te and len(message_te) > 4096:
            raise ValidationError('Telugu message is too long (max 4096 characters)')
        
        # Validate phone numbers based on mode
        if sending_mode == 'single':
            if not phone_number:
                raise ValidationError('Please enter a phone number')
            if not phone_number.isdigit() or len(phone_number) < 10:
                raise ValidationError('Invalid phone number format')
        
        elif sending_mode == 'multiple':
            if not phone_numbers:
                raise ValidationError('Please enter phone numbers')
            numbers = [n.strip() for n in phone_numbers.replace(',', '\n').split('\n') if n.strip()]
            if not numbers:
                raise ValidationError('Please enter at least one phone number')
            invalid_numbers = [n for n in numbers if not n.isdigit() or len(n) < 10]
            if invalid_numbers:
                raise ValidationError(f'Invalid phone numbers: {", ".join(invalid_numbers[:5])}')
        
        elif sending_mode == 'file':
            if not phone_file:
                raise ValidationError('Please upload a file')
        
        return cleaned_data

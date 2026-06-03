from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator
import os


class SchoolSetting(models.Model):
    """Store school information and settings"""
    school_name = models.CharField(max_length=255)
    school_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    admin_user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.school_name

    class Meta:
        verbose_name_plural = "School Settings"


class Contact(models.Model):
    """Store parent/student contact information"""
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('te', 'Telugu'),
    ]

    name = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\d{10,15}$',
            message='Phone number must be 10-15 digits'
        )]
    )
    email = models.EmailField(blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    school = models.ForeignKey(SchoolSetting, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        unique_together = ('phone', 'school')
        ordering = ['-created_at']


class BulkMessage(models.Model):
    """Store bulk message templates and history"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    school = models.ForeignKey(SchoolSetting, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message_en = models.TextField(help_text="Message in English")
    message_te = models.TextField(blank=True, help_text="Message in Telugu")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_time = models.DateTimeField(blank=True, null=True)
    
    total_contacts = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    class Meta:
        ordering = ['-created_at']

    @property
    def pending_count(self):
        return self.total_contacts - self.sent_count - self.failed_count


class MessageLog(models.Model):
    """Log individual message sending attempts"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('blocked', 'Blocked'),
    ]

    bulk_message = models.ForeignKey(BulkMessage, on_delete=models.CASCADE, related_name='logs')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    attempt_count = models.IntegerField(default=0)
    last_attempted_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact.phone} - {self.status}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('bulk_message', 'contact')


class ActivityLog(models.Model):
    """Log all admin activities for auditing"""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('upload', 'Contact Upload'),
        ('send', 'Message Send'),
        ('delete', 'Delete Contacts'),
        ('export', 'Export Report'),
    ]

    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin_user.username} - {self.action}"

    class Meta:
        ordering = ['-created_at']


class HolidayTemplate(models.Model):
    """Holiday notice templates for quick messaging"""
    school = models.ForeignKey(SchoolSetting, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    message_en = models.TextField(help_text="Holiday notice in English")
    message_te = models.TextField(blank=True, help_text="Holiday notice in Telugu")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

"""
Django admin configuration for WhatsApp notification system
"""

from django.contrib import admin
from .models import (
    SchoolSetting, Contact, BulkMessage, 
    MessageLog, ActivityLog, HolidayTemplate
)


@admin.register(SchoolSetting)
class SchoolSettingAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'admin_user', 'created_at')
    search_fields = ('school_name', 'admin_user__username')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'language', 'school', 'is_blocked', 'created_at')
    list_filter = ('school', 'language', 'is_blocked', 'created_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BulkMessage)
class BulkMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'status', 'total_contacts', 'sent_count', 'failed_count', 'created_at')
    list_filter = ('school', 'status', 'created_at')
    search_fields = ('title', 'message_en', 'message_te')
    readonly_fields = ('created_at', 'updated_at', 'started_at', 'completed_at')
    fields = (
        'school', 'title', 'message_en', 'message_te', 'status',
        'total_contacts', 'sent_count', 'failed_count',
        'scheduled_time', 'created_by',
        'created_at', 'updated_at', 'started_at', 'completed_at'
    )


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('bulk_message', 'contact', 'status', 'last_attempted_at', 'sent_at')
    list_filter = ('status', 'bulk_message', 'created_at')
    search_fields = ('contact__name', 'contact__phone')
    readonly_fields = ('created_at', 'last_attempted_at', 'sent_at')


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('admin_user', 'action', 'created_at', 'ip_address')
    list_filter = ('action', 'admin_user', 'created_at')
    search_fields = ('admin_user__username', 'description')
    readonly_fields = ('created_at',)


@admin.register(HolidayTemplate)
class HolidayTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'created_at')
    list_filter = ('school', 'created_at')
    search_fields = ('name', 'message_en', 'message_te')
    readonly_fields = ('created_at', 'updated_at')

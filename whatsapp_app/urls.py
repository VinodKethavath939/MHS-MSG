"""
URL configuration for whatsapp_app
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Contacts
    path('contacts/', views.contacts_list, name='contacts_list'),
    path('contacts/upload/', views.upload_contacts, name='upload_contacts'),
    path('contacts/delete/<int:contact_id>/', views.delete_contacts, name='delete_contact'),
    path('contacts/delete/', views.delete_contacts, name='delete_contacts'),
    
    # Messages
    path('messages/', views.messages_list, name='messages_list'),
    path('messages/create/', views.create_message, name='create_message'),
    path('messages/send-direct/', views.send_direct_message, name='send_direct_message'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
    path('messages/<int:message_id>/send/', views.send_message, name='send_message'),
    path('messages/<int:message_id>/export/', views.export_report, name='export_report'),
    
    # Templates
    path('templates/', views.templates_list, name='templates_list'),
    path('templates/create/', views.create_template, name='create_template'),
    
    # API endpoints
    path('api/message/<int:message_id>/progress/', views.api_message_progress, name='api_message_progress'),
    path('api/contacts/stats/', views.api_contacts_stats, name='api_contacts_stats'),
]

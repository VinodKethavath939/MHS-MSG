"""
Management command to initialize the application
Usage: python manage.py initialize_app
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from whatsapp_app.models import SchoolSetting, HolidayTemplate
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Initialize the WhatsApp notification system'

    def handle(self, *args, **options):
        self.stdout.write("Starting application initialization...")
        
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@school.local', 'admin123')
            self.stdout.write(self.style.SUCCESS('✓ Created admin user (admin / admin123)'))
        else:
            self.stdout.write('✓ Admin user already exists')
        
        # Create school setting
        try:
            admin = User.objects.get(username='admin')
            if not SchoolSetting.objects.filter(admin_user=admin).exists():
                school = SchoolSetting.objects.create(
                    school_name='My School',
                    admin_user=admin
                )
                self.stdout.write(self.style.SUCCESS('✓ Created school setting'))
            else:
                self.stdout.write('✓ School setting already exists')
                school = SchoolSetting.objects.get(admin_user=admin)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('✗ Admin user not found'))
            return
        
        # Create sample templates
        templates_data = [
            {
                'name': 'Holiday Announcement',
                'message_en': 'Dear Parents, School will remain closed for holidays. Regular classes will resume on [DATE]. We wish you a wonderful time with your family.',
                'message_te': 'ప్రియ తల్లిదండ్రులు, విద్యాలయం ఛుట్టీలకు మూసి ఉంటుంది. సాధారణ తరగతులు [DATE] నుండి తిరిగి ప్రారంభమవుతాయి. మీరు కుటుంబంతో అద్భుతమైన సమయం గడపాలని కోరుకుంటున్నాం.'
            },
            {
                'name': 'Exam Schedule Notice',
                'message_en': 'Dear Parents, The [SUBJECT] exams will be held on [DATE] from [TIME]. Please ensure your child studies well and reaches school on time.',
                'message_te': 'ప్రియ తల్లిదండ్రులు, [SUBJECT] పరీక్షలు [DATE] నాడు [TIME] కు నిర్వహించబడతాయి. దయచేసి మీ బిడ్డ బాగా చదువు మరియు సమయానికి పాఠశాలకు చేరుకోని కోసం సూచించండి.'
            },
            {
                'name': 'Fee Reminder',
                'message_en': 'Dear Parents, This is a friendly reminder to submit school fees by [DATE]. For any queries regarding fee structure or payment options, please contact the office.',
                'message_te': 'ప్రియ తల్లిదండ్రులు, ఇది [DATE] నాటికి పాఠశాల ఫీ సమర్పించమని స్నేహపూర్వక జ్ఞప్తి. ఫీ నిర్మాణం లేదా చెల్లింపు ఎంపికల గురించి ఏవైనా ప్రశ్నలకు, దయచేసి కార్యాలయానికి సంప్రదించండి.'
            },
            {
                'name': 'Event Announcement',
                'message_en': 'Dear Parents, We are organizing [EVENT NAME] on [DATE] at [TIME] at [VENUE]. Your child\'s participation will help them develop new skills. Please encourage them to participate.',
                'message_te': 'ప్రియ తల్లిదండ్రులు, మేము [EVENT NAME] ను [DATE] నాడు [TIME] కు [VENUE] వద్ద నిర్వహిస్తున్నాము. మీ బిడ్డ భాగస్వామ్యం వారికి కొత్త నైపుణ్యాలను అభివృద్ధి చేయడానికి సహాయపడుతుంది. దయచేసి వారిని భాగస్వామ్యం చేయమని ప్రోత్సహించండి.'
            }
        ]
        
        created_count = 0
        for template_data in templates_data:
            if not HolidayTemplate.objects.filter(
                school=school,
                name=template_data['name']
            ).exists():
                HolidayTemplate.objects.create(
                    school=school,
                    **template_data
                )
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} message templates'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Application initialization completed!'))
        self.stdout.write('You can now login with: admin / admin123')

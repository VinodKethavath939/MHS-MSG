"""
Test data and sample utilities for development
"""

# Sample Excel file data structure
SAMPLE_CONTACTS_EN = [
    {'name': 'Rajesh Kumar', 'phone': '9876543210'},
    {'name': 'Priya Singh', 'phone': '9123456789'},
    {'name': 'Amit Patel', 'phone': '9988776655'},
    {'name': 'Neha Sharma', 'phone': '9876654321'},
    {'name': 'Vikram Gupta', 'phone': '9765432109'},
]

SAMPLE_TEMPLATES = [
    {
        'name': 'Holiday Announcement',
        'message_en': 'Dear Parents, School will remain closed from January 26 to February 2 for Republic Day holidays. Regular classes will resume on February 3. We wish you a wonderful time with your family.',
        'message_te': 'ప్రియ తల్లిదండ్రులు, రిపబ్లిక్ డే ఛుట్టీల కోసం జనవరి 26 నుండి ఫిబ్రువరి 2 వరకు పాఠశాల మూసి ఉంటుంది. సాధారణ తరగతులు ఫిబ్రువరి 3 నుండి తిరిగి ప్రారంభమవుతాయి. మీరు కుటుంబంతో అద్భుతమైన సమయం గడపాలని కోరుకుంటున్నాము.'
    },
    {
        'name': 'Exam Schedule Notice',
        'message_en': 'Dear Parents, The Annual Examinations for Class 10 will begin from March 1. Please ensure your child studies well and reaches school on time. All the best!',
        'message_te': 'ప్రియ తల్లిదండ్రులు, 10వ తరగతి వార్షిక పరీక్షలు మార్చి 1 నుండి ప్రారంభమవుతాయి. దయచేసి మీ బిడ్డ బాగా చదువు మరియు సమయానికి పాఠశాలకు చేరుకోని కోసం సూచించండి. ఉత్తమ విజయాలు!'
    },
    {
        'name': 'Fee Reminder',
        'message_en': 'Dear Parents, This is a friendly reminder to submit school fees by January 15. For any queries regarding fee structure or payment options, please contact the office.',
        'message_te': 'ప్రియ తల్లిదండ్రులు, ఇది జనవరి 15 నాటికి పాఠశాల ఫీ సమర్పించమని స్నేహపూర్వక జ్ఞప్తి. ఫీ నిర్మాణం లేదా చెల్లింపు ఎంపికల గురించి ఏవైనా ప్రశ్నలకు, దయచేసి కార్యాలయానికి సంప్రదించండి.'
    },
    {
        'name': 'Annual Day Announcement',
        'message_en': 'Dear Parents, We are delighted to invite you for our Annual Day celebration on April 15. Your child\'s participation will help them develop new skills. Please encourage them to participate and mark the date.',
        'message_te': 'ప్రియ తల్లిదండ్రులు, మేము ఏప్రిల్ 15 నాడు మా వార్షిక దిన వేడుక కు జీవితమీద ఆహ్వానం చేయటానికి ఆనందితులను. మీ బిడ్డ భాగస్వామ్యం వారికి కొత్త నైపుణ్యాలను అభివృద్ధి చేయడానికి సహాయపడుతుంది. దయచేసి వారిని భాగస్వామ్యం చేయమని ప్రోత్సహించండి మరియు తేదీని గుర్తుంచుకోండి.'
    },
]


def create_sample_excel_file(filepath='sample_contacts.xlsx'):
    """
    Create a sample Excel file for testing
    Requires openpyxl
    """
    try:
        from openpyxl import Workbook
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Contacts"
        
        # Add headers
        ws['A1'] = "Name"
        ws['B1'] = "Phone"
        
        # Add sample data
        for idx, contact in enumerate(SAMPLE_CONTACTS_EN, start=2):
            ws[f'A{idx}'] = contact['name']
            ws[f'B{idx}'] = contact['phone']
        
        wb.save(filepath)
        print(f"✓ Sample Excel file created: {filepath}")
        return True
    except ImportError:
        print("✗ openpyxl not installed. Run: pip install openpyxl")
        return False


def create_sample_csv_file(filepath='sample_contacts.csv'):
    """
    Create a sample CSV file for testing
    """
    import csv
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Name', 'Phone'])
            writer.writeheader()
            writer.writerows(SAMPLE_CONTACTS_EN)
        
        print(f"✓ Sample CSV file created: {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error creating CSV file: {str(e)}")
        return False


# Demo credentials
DEMO_ADMIN = {
    'username': 'admin',
    'password': 'admin123',
    'email': 'admin@school.local'
}

# Sample phone formats
PHONE_FORMATS = {
    'India': {
        '10_digit': '9876543210',
        '12_digit': '919876543210',
        'with_plus': '+919876543210',
        'country_code': '91',
    },
    'US': {
        '10_digit': '2015551234',
        'country_code': '1',
    },
    'UK': {
        '10_digit': '2071234567',
        'country_code': '44',
    }
}

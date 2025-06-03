import sqlite3
from datetime import datetime, timedelta
import hashlib
import secrets
import random
import os
import json
from werkzeug.security import generate_password_hash

def hash_password(password):
    """Hash password with salt for secure storage"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return hash_obj.hexdigest(), salt

def gen_patient_id():
    """Generate a random 7-digit patient_id as a string"""
    return str(random.randint(1000000, 9999999))

def generate_unique_bill_number():
    """Generate a unique 6-digit bill number"""
    return str(random.randint(100000, 999999))

def init_test_data():
    """Initialize comprehensive test data for the SignalWire dental office system"""
    conn = sqlite3.connect('dental_office.db')
    cursor = conn.cursor()

    print("Initializing comprehensive test data...")

    # Read and execute schema.sql
    with open('schema.sql', 'r') as f:
        schema = f.read()
        cursor.executescript(schema)

    # Apply bill_number migration if it exists
    try:
        # Check if bill_number column already exists
        cursor.execute("PRAGMA table_info(billing)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'bill_number' not in columns:
            print("Adding bill_number column to billing table...")
            cursor.execute("ALTER TABLE billing ADD COLUMN bill_number TEXT")
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_billing_bill_number ON billing(bill_number)")
            conn.commit()
        else:
            print("bill_number column already exists")
    except sqlite3.Error as e:
        print(f"Migration note: {e}")
        pass  # Continue with data insertion

    # Insert comprehensive dental services
    services = [
        ('Regular Cleaning', 'Standard dental cleaning and checkup', 120.00, 'cleaning'),
        ('Deep Cleaning', 'Deep cleaning and scaling for gum disease', 250.00, 'cleaning'),
        ('Cavity Filling', 'Composite filling for cavities', 180.00, 'filling'),
        ('Root Canal', 'Root canal treatment for infected teeth', 950.00, 'root_canal'),
        ('Teeth Whitening', 'Professional teeth whitening treatment', 350.00, 'whitening'),
        ('Dental Checkup', 'Comprehensive dental examination', 85.00, 'checkup'),
        ('Crown Installation', 'Dental crown installation', 1200.00, 'other'),
        ('Tooth Extraction', 'Simple tooth extraction', 200.00, 'extraction'),
        ('Wisdom Tooth Removal', 'Surgical wisdom tooth extraction', 400.00, 'extraction'),
        ('Dental Implant', 'Single tooth implant with crown', 3500.00, 'other'),
        ('Braces Consultation', 'Orthodontic consultation and planning', 150.00, 'orthodontics'),
        ('Emergency Visit', 'Emergency dental treatment', 200.00, 'other')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO dental_services (name, description, price, type)
        VALUES (?, ?, ?, ?)
    ''', services)

    # Enhanced working hours for different dentists
    dr_smith_hours = json.dumps({
        "monday": {"morning": True, "afternoon": True, "evening": False},
        "tuesday": {"morning": True, "afternoon": True, "evening": False},
        "wednesday": {"morning": True, "afternoon": True, "evening": False},
        "thursday": {"morning": True, "afternoon": True, "evening": False},
        "friday": {"morning": True, "afternoon": True, "evening": False},
        "saturday": {"morning": False, "afternoon": False, "evening": False},
        "sunday": {"morning": False, "afternoon": False, "evening": False}
    })
    
    dr_johnson_hours = json.dumps({
        "monday": {"morning": True, "afternoon": True, "evening": True},
        "tuesday": {"morning": True, "afternoon": True, "evening": True},
        "wednesday": {"morning": True, "afternoon": True, "evening": True},
        "thursday": {"morning": True, "afternoon": True, "evening": True},
        "friday": {"morning": True, "afternoon": True, "evening": False},
        "saturday": {"morning": False, "afternoon": False, "evening": False},
        "sunday": {"morning": False, "afternoon": False, "evening": False}
    })
    
    dr_chen_hours = json.dumps({
        "monday": {"morning": True, "afternoon": True, "evening": False},
        "tuesday": {"morning": True, "afternoon": True, "evening": False},
        "wednesday": {"morning": True, "afternoon": True, "evening": False},
        "thursday": {"morning": True, "afternoon": True, "evening": False},
        "friday": {"morning": True, "afternoon": False, "evening": False},
        "saturday": {"morning": False, "afternoon": False, "evening": False},
        "sunday": {"morning": False, "afternoon": False, "evening": False}
    })

    # Insert comprehensive dentist data
    dentist_password_hash, dentist_password_salt = hash_password('dentist123')
    dentists = [
        ('Dr. John', 'Smith', 'dr.smith@dentaloffice.com', '555-0101', 
         'General Dentistry', 'DENT123456', 
         dentist_password_hash, dentist_password_salt, dr_smith_hours),
        ('Dr. Sarah', 'Johnson', 'dr.johnson@dentaloffice.com', '555-0103',
         'Orthodontics', 'DENT654321',
         dentist_password_hash, dentist_password_salt, dr_johnson_hours),
        ('Dr. Michael', 'Chen', 'dr.chen@dentaloffice.com', '555-0105',
         'Oral Surgery', 'DENT789012',
         dentist_password_hash, dentist_password_salt, dr_chen_hours)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO dentists (first_name, last_name, email, phone, specialization, 
                            license_number, password_hash, password_salt, working_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dentists)

    # Insert comprehensive patient data
    patient_password_hash, patient_password_salt = hash_password('patient123')
    patients = [
        ('Jane', 'Doe', 'jane.doe@email.com', '555-0102', 
         '123 Main St, Anytown, USA', '1990-01-01',
         'No known allergies', 'Insurance Provider: DentalCare Plus, Policy: DC123456',
         patient_password_hash, patient_password_salt, '8675309'),
        ('Jim', 'Smith', 'jim.smith@email.com', '555-0104',
         '456 Elm St, Anytown, USA', '1985-05-15',
         'Penicillin allergy', 'Insurance Provider: HealthFirst, Policy: HF789012',
         patient_password_hash, patient_password_salt, gen_patient_id()),
        ('Maria', 'Garcia', 'maria.garcia@email.com', '555-0106',
         '789 Oak Ave, Anytown, USA', '1992-08-22',
         'Latex allergy, diabetes', 'Insurance Provider: MediCare Dental, Policy: MD345678',
         patient_password_hash, patient_password_salt, gen_patient_id()),
        ('Robert', 'Wilson', 'robert.wilson@email.com', '555-0108',
         '321 Pine St, Anytown, USA', '1978-11-30',
         'High blood pressure, takes medication', 'Insurance Provider: DentalCare Plus, Policy: DC901234',
         patient_password_hash, patient_password_salt, gen_patient_id()),
        ('Emily', 'Brown', 'emily.brown@email.com', '555-0110',
         '654 Maple Dr, Anytown, USA', '1995-03-18',
         'No known allergies', 'No insurance',
         patient_password_hash, patient_password_salt, gen_patient_id())
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO patients (first_name, last_name, email, phone, address, 
                            date_of_birth, medical_history, insurance_info, 
                            password_hash, password_salt, patient_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', patients)

    # Insert comprehensive payment methods
    payment_methods = [
        # Jane Doe's payment methods
        (1, 'credit_card', '4111111111111111', '12/25', 'Jane Doe', None, None, None, 1),
        (1, 'credit_card', '4532123456789014', '09/26', 'Jane Doe', None, None, None, 0),
        (1, 'banking', None, None, None, 'Chase Bank', '9876543210', '021000021', 0),
        
        # Jim Smith's payment methods
        (2, 'credit_card', '4532123456789015', '03/26', 'Jim Smith', None, None, None, 1),
        (2, 'banking', None, None, None, 'Bank of America', '1234567890', '026009593', 0),
        
        # Maria Garcia's payment methods
        (3, 'credit_card', '4000000000000002', '08/25', 'Maria Garcia', None, None, None, 1),
        (3, 'banking', None, None, None, 'Wells Fargo', '5555666677', '121000248', 0),
        
        # Robert Wilson's payment methods
        (4, 'credit_card', '4242424242424242', '11/27', 'Robert Wilson', None, None, None, 1),
        
        # Emily Brown's payment methods
        (5, 'credit_card', '4012888888881881', '05/25', 'Emily Brown', None, None, None, 1)
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO payment_methods 
    (patient_id, method_type, card_number, expiry_date, card_holder, bank_name, account_number, routing_number, is_default)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', payment_methods)

    # Insert comprehensive appointments
    now = datetime.now()
    appointments = [
        # Upcoming appointments
        (1, 1, 1, 'scheduled',
         (now + timedelta(days=3)).strftime('%Y-%m-%d 09:00:00'),
         (now + timedelta(days=3)).strftime('%Y-%m-%d 10:00:00'),
         'Regular 6-month cleaning', 1),
        (2, 1, 3, 'scheduled',
         (now + timedelta(days=7)).strftime('%Y-%m-%d 14:00:00'),
         (now + timedelta(days=7)).strftime('%Y-%m-%d 15:30:00'),
         'Cavity filling on molar', 1),
        (3, 2, 11, 'scheduled',
         (now + timedelta(days=10)).strftime('%Y-%m-%d 11:00:00'),
         (now + timedelta(days=10)).strftime('%Y-%m-%d 12:00:00'),
         'Braces consultation', 1),
        (4, 3, 8, 'scheduled',
         (now + timedelta(days=14)).strftime('%Y-%m-%d 15:00:00'),
         (now + timedelta(days=14)).strftime('%Y-%m-%d 16:00:00'),
         'Wisdom tooth extraction', 1),
        
        # Today's appointments
        (1, 1, 6, 'scheduled',
         now.strftime('%Y-%m-%d 10:00:00'),
         now.strftime('%Y-%m-%d 11:00:00'),
         'Annual checkup', 1),
        (5, 1, 12, 'scheduled',
         now.strftime('%Y-%m-%d 14:00:00'),
         now.strftime('%Y-%m-%d 15:00:00'),
         'Emergency toothache', 1),
        
        # Recent completed appointments
        (1, 1, 1, 'completed',
         (now - timedelta(days=180)).strftime('%Y-%m-%d 09:00:00'),
         (now - timedelta(days=180)).strftime('%Y-%m-%d 10:00:00'),
         'Previous cleaning - excellent condition', 1),
        (2, 1, 6, 'completed',
         (now - timedelta(days=30)).strftime('%Y-%m-%d 13:00:00'),
         (now - timedelta(days=30)).strftime('%Y-%m-%d 14:00:00'),
         'Checkup revealed cavity', 1),
        (3, 2, 5, 'completed',
         (now - timedelta(days=45)).strftime('%Y-%m-%d 16:00:00'),
         (now - timedelta(days=45)).strftime('%Y-%m-%d 17:30:00'),
         'Teeth whitening completed successfully', 1),
        (4, 1, 4, 'in_progress',
         (now - timedelta(days=7)).strftime('%Y-%m-%d 10:00:00'),
         (now - timedelta(days=7)).strftime('%Y-%m-%d 12:00:00'),
         'Root canal treatment started', 1),
        
        # Cancelled appointment
        (5, 2, 1, 'cancelled',
         (now - timedelta(days=15)).strftime('%Y-%m-%d 14:00:00'),
         (now - timedelta(days=15)).strftime('%Y-%m-%d 15:00:00'),
         'Patient cancelled due to illness', 0)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO appointments (patient_id, dentist_id, service_id,
                                status, start_time, end_time, notes, sms_reminder)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', appointments)

    # Insert comprehensive treatment history
    treatments = [
        # Jane Doe's treatments
        (1, 1, 1, (now - timedelta(days=180)).strftime('%Y-%m-%d'),
         'Routine cleaning', 'Excellent oral hygiene. No issues found.', 
         (now + timedelta(days=180)).strftime('%Y-%m-%d'), 'TH001', 120.00),
        (1, 1, 6, (now - timedelta(days=30)).strftime('%Y-%m-%d'),
         'Annual checkup', 'Overall good health. Recommended whitening.', 
         (now + timedelta(days=180)).strftime('%Y-%m-%d'), 'TH002', 85.00),
         
        # Jim Smith's treatments
        (2, 1, 6, (now - timedelta(days=30)).strftime('%Y-%m-%d'),
         'Checkup revealed cavity', 'Small cavity found in upper right molar',
         (now + timedelta(days=7)).strftime('%Y-%m-%d'), 'TH003', 85.00),
        (2, 1, 2, (now - timedelta(days=90)).strftime('%Y-%m-%d'),
         'Deep cleaning', 'Moderate tartar buildup removed successfully',
         (now + timedelta(days=120)).strftime('%Y-%m-%d'), 'TH004', 250.00),
        (2, 1, 3, (now).strftime('%Y-%m-%d'),
         'Cavity filling', 'Composite filling placed in upper right molar',
         (now + timedelta(days=180)).strftime('%Y-%m-%d'), 'TH_FUTURE_001', 180.00),
         
        # Maria Garcia's treatments
        (3, 2, 5, (now - timedelta(days=45)).strftime('%Y-%m-%d'),
         'Teeth whitening', 'Professional whitening completed. Excellent results.',
         None, 'TH005', 350.00),
        (3, 2, 1, (now - timedelta(days=120)).strftime('%Y-%m-%d'),
         'Regular cleaning', 'Good oral health maintained.',
         (now + timedelta(days=60)).strftime('%Y-%m-%d'), 'TH006', 120.00),
         
        # Robert Wilson's treatments
        (4, 1, 4, (now - timedelta(days=7)).strftime('%Y-%m-%d'),
         'Root canal treatment', 'Root canal procedure initiated. Follow-up required.',
         (now + timedelta(days=14)).strftime('%Y-%m-%d'), 'TH007', 950.00),
        (4, 3, 8, (now - timedelta(days=60)).strftime('%Y-%m-%d'),
         'Tooth extraction', 'Extracted damaged tooth #18',
         (now + timedelta(days=30)).strftime('%Y-%m-%d'), 'TH008', 200.00),
         
        # Emily Brown's treatments
        (5, 1, 12, (now - timedelta(days=5)).strftime('%Y-%m-%d'),
         'Emergency toothache', 'Provided pain relief and temporary filling',
         (now + timedelta(days=7)).strftime('%Y-%m-%d'), 'TH009', 200.00),
         
        # Additional overdue treatments
        (1, 1, 1, (now - timedelta(days=90)).strftime('%Y-%m-%d'),
         'Previous cleaning', 'Routine cleaning performed successfully.',
         (now + timedelta(days=90)).strftime('%Y-%m-%d'), 'TH_OVERDUE_001', 150.00),
        (4, 1, 6, (now - timedelta(days=75)).strftime('%Y-%m-%d'),
         'Overdue checkup', 'Regular examination completed.',
         (now + timedelta(days=180)).strftime('%Y-%m-%d'), 'TH_OVERDUE_002', 85.00)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO treatment_history (patient_id, dentist_id, service_id,
                                     treatment_date, diagnosis, treatment_notes,
                                     follow_up_date, reference_number, bill_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', treatments)

    # Insert comprehensive billing records with 6-digit bill numbers
    billing = [
        # Jane Doe's bills
        (1, 1, 1, 1, 120.00, 80.00, 0.00, 'paid', 
         (now - timedelta(days=150)).strftime('%Y-%m-%d'), 'TH001', 
         (now - timedelta(days=180)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
        (1, 1, 5, 6, 85.00, 60.00, 0.00, 'paid', 
         (now).strftime('%Y-%m-%d'), 'TH002', 
         (now - timedelta(days=30)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
         
        # Jim Smith's bills
        (2, 1, 8, 6, 85.00, 70.00, 15.00, 'partial', 
         (now).strftime('%Y-%m-%d'), 'TH003', 
         (now - timedelta(days=30)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
        (2, 1, 4, 2, 250.00, 150.00, 0.00, 'paid', 
         (now - timedelta(days=60)).strftime('%Y-%m-%d'), 'TH004', 
         (now - timedelta(days=90)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
        (2, 1, None, 3, 180.00, 120.00, 60.00, 'pending', 
         (now + timedelta(days=30)).strftime('%Y-%m-%d'), 'TH_FUTURE_001', 
         (now).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
         
        # Maria Garcia's bills
        (3, 2, 9, 5, 350.00, 0.00, 0.00, 'paid', 
         (now - timedelta(days=15)).strftime('%Y-%m-%d'), 'TH005', 
         (now - timedelta(days=45)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
        (3, 2, 6, 1, 120.00, 80.00, 40.00, 'pending', 
         (now + timedelta(days=30)).strftime('%Y-%m-%d'), 'TH006', 
         (now - timedelta(days=120)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
         
        # Robert Wilson's bills
        (4, 1, 10, 4, 950.00, 600.00, 200.00, 'partial', 
         (now + timedelta(days=30)).strftime('%Y-%m-%d'), 'TH007', 
         (now - timedelta(days=7)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
        (4, 3, 7, 8, 200.00, 150.00, 0.00, 'paid', 
         (now - timedelta(days=30)).strftime('%Y-%m-%d'), 'TH008', 
         (now - timedelta(days=60)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
         
        # Emily Brown's bills (no insurance)
        (5, 1, 11, 12, 200.00, 0.00, 200.00, 'overdue', 
         (now - timedelta(days=10)).strftime('%Y-%m-%d'), 'TH009', 
         (now - timedelta(days=5)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
         
        # Additional overdue bills for testing
        (1, 1, None, 1, 150.00, 100.00, 50.00, 'overdue', 
         (now - timedelta(days=45)).strftime('%Y-%m-%d'), 'TH_OVERDUE_001', 
         (now - timedelta(days=90)).strftime('%Y-%m-%d'), None, generate_unique_bill_number()),
        (4, 1, None, 6, 85.00, 85.00, 0.00, 'overdue', 
         (now - timedelta(days=30)).strftime('%Y-%m-%d'), 'TH_OVERDUE_002', 
         (now - timedelta(days=75)).strftime('%Y-%m-%d'), None, generate_unique_bill_number())
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO billing (patient_id, dentist_id, appointment_id, service_id, amount,
                           insurance_coverage, patient_portion, status, due_date, reference_number,
                           created_at, payment_id, bill_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', billing)

    # Insert comprehensive payment history
    payment_records = [
        # Jane Doe's payments
        (1, 1, 40.00, (now - timedelta(days=170)).strftime('%Y-%m-%d %H:%M:%S'), 1, 'credit_card', 'completed', 'TXN100001', 'Paid insurance copay for cleaning'),
        (2, 1, 25.00, (now - timedelta(days=25)).strftime('%Y-%m-%d %H:%M:%S'), 1, 'credit_card', 'completed', 'TXN100002', 'Paid copay for checkup'),
        
        # Jim Smith's payments
        (3, 2, 70.00, (now - timedelta(days=25)).strftime('%Y-%m-%d %H:%M:%S'), 4, 'credit_card', 'completed', 'TXN100003', 'Partial payment for checkup'),
        (4, 2, 100.00, (now - timedelta(days=55)).strftime('%Y-%m-%d %H:%M:%S'), 4, 'credit_card', 'completed', 'TXN100004', 'Paid patient portion for deep cleaning'),
        (8, 4, 150.00, (now - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'), 4, 'banking', 'completed', 'TXN100005', 'Partial payment for root canal'),
        
        # Maria Garcia's payments
        (6, 3, 350.00, (now - timedelta(days=40)).strftime('%Y-%m-%d %H:%M:%S'), 6, 'credit_card', 'completed', 'TXN100006', 'Full payment for teeth whitening'),
        
        # Robert Wilson's payments
        (9, 4, 50.00, (now - timedelta(days=25)).strftime('%Y-%m-%d %H:%M:%S'), 8, 'credit_card', 'completed', 'TXN100007', 'Paid copay for extraction'),
        (8, 4, 200.00, (now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'), 8, 'credit_card', 'completed', 'TXN100008', 'Second payment for root canal'),
        
        # Failed payment example
        (10, 5, 200.00, (now - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'), 9, 'credit_card', 'failed', 'TXN100009', 'Payment failed - insufficient funds')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO payments (billing_id, patient_id, amount, payment_date, 
                                      payment_method_id, payment_method_type, status, 
                                      transaction_id, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', payment_records)

    # Insert comprehensive insurance claims
    insurance_claims = [
        (1, 80.00, 'approved', (now - timedelta(days=175)).strftime('%Y-%m-%d'), 
         (now - timedelta(days=165)).strftime('%Y-%m-%d'), 'Claim for routine cleaning approved'),
        (2, 60.00, 'approved', (now - timedelta(days=35)).strftime('%Y-%m-%d'), 
         (now - timedelta(days=20)).strftime('%Y-%m-%d'), 'Claim for checkup approved'),
        (3, 70.00, 'pending', (now - timedelta(days=25)).strftime('%Y-%m-%d'),
         None, 'Claim for checkup under review'),
        (4, 150.00, 'approved', (now - timedelta(days=85)).strftime('%Y-%m-%d'),
         (now - timedelta(days=70)).strftime('%Y-%m-%d'), 'Claim for deep cleaning approved'),
        (5, 120.00, 'pending', (now - timedelta(days=5)).strftime('%Y-%m-%d'),
         None, 'Claim for cavity filling submitted'),
        (7, 80.00, 'pending', (now - timedelta(days=115)).strftime('%Y-%m-%d'),
         None, 'Claim for cleaning under review'),
        (8, 600.00, 'pending', (now - timedelta(days=5)).strftime('%Y-%m-%d'),
         None, 'Claim for root canal submitted'),
        (9, 150.00, 'approved', (now - timedelta(days=55)).strftime('%Y-%m-%d'),
         (now - timedelta(days=40)).strftime('%Y-%m-%d'), 'Claim for extraction approved'),
        (11, 100.00, 'rejected', (now - timedelta(days=85)).strftime('%Y-%m-%d'),
         (now - timedelta(days=75)).strftime('%Y-%m-%d'), 'Claim rejected - not covered service'),
        (12, 85.00, 'approved', (now - timedelta(days=70)).strftime('%Y-%m-%d'),
         (now - timedelta(days=60)).strftime('%Y-%m-%d'), 'Claim for overdue checkup approved')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO insurance_claims (billing_id, claim_amount, status, submission_date, 
                                    response_date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', insurance_claims)

    conn.commit()
    conn.close()
    
    print("✓ Comprehensive test data initialization completed!")
    print("\n=== Test Data Summary ===")
    print("• 3 Dentists with different specializations")
    print("• 5 Patients with diverse backgrounds")
    print("• 12 Dental services covering all treatment types") 
    print("• 11 Appointments (past, present, and future)")
    print("• 9 Treatment history records")
    print("• 12 Bills with 6-digit bill numbers")
    print("• 9 Payment records (including one failed)")
    print("• 10 Insurance claims with various statuses")
    print("• 9 Payment methods across all patients")
    print("\n=== Login Credentials ===")
    print("Dentist: dr.smith@dentaloffice.com / dentist123")
    print("Patient: jane.doe@email.com / patient123")
    print("=============================")

if __name__ == '__main__':
    init_test_data()

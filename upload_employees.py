import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import os

# 1. Setup Firebase Admin
cred_path = 'majed-code1-service-key.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def upload_data():
    # Use the file that HAS emails
    file_path = r'C:\Users\majed.altaifi\Desktop\Nesma Reports MAIN Data.xlsx'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return

    print(f"Reading {file_path} (with emails)...")
    df = pd.read_excel(file_path)
    
    batch = db.batch()
    count = 0
    total = 0
    
    print("Starting upload to Firestore (majed-code1)...")
    
    for _, row in df.iterrows():
        emp_no = str(row.get('Employee Code', '')).strip()
        if not emp_no or emp_no == 'nan' or emp_no == '': continue
        if '.' in emp_no: emp_no = emp_no.split('.')[0]
        
        doc_ref = db.collection('employees').document(emp_no)
        
        # Capture email for Forgot Password functionality
        email = str(row.get('E-Mail', '')).strip().lower()
        if email == 'nan' or email == '': email = None

        payload = {
            'emp_no': emp_no,
            'name_en': str(row.get('Employee Name - English', '')).strip(),
            'role': str(row.get('Position - English', '')).strip(),
            'department': str(row.get('Departments - English', '')).strip(),
            'division': str(row.get('Division - English', '')).strip(),
            'site': str(row.get('Site - English', '')).strip(),
            'project': str(row.get('Project - English', '')).strip(),
            'email': email,
            'phone': str(row.get('Mobile', '')).strip(),
            'grade': str(row.get('Grade - English', '')).strip(),
            'activated': False,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        batch.set(doc_ref, payload, merge=True)
        count += 1
        total += 1
        
        if count >= 400:
            batch.commit()
            print(f"Uploaded {total} records with emails...")
            batch = db.batch()
            count = 0
            
    if count > 0:
        batch.commit()
        
    print(f"DONE! {total} employees with emails uploaded to majed-code1.")

if __name__ == "__main__":
    upload_data()

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
    file_path = r'C:\Users\majed.altaifi\Desktop\System_Employees_Sites.xlsx'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return

    print(f"Reading {file_path}...")
    df = pd.read_excel(file_path)
    
    batch = db.batch()
    count = 0
    total = 0
    
    print("Starting upload to Firestore (majed-code1)...")
    
    for _, row in df.iterrows():
        # Using the actual column names from the file
        emp_no = str(row.get('Emp Code', '')).strip()
        if not emp_no or emp_no == 'nan' or emp_no == '': continue
        
        # Remove any decimal point if it exists (like 2838.0)
        if '.' in emp_no: emp_no = emp_no.split('.')[0]
        
        doc_ref = db.collection('employees').document(emp_no)
        
        payload = {
            'emp_no': emp_no,
            'name_en': str(row.get('Employee Name', '')).strip(),
            'role': str(row.get('Position', '')).strip(),
            'department': str(row.get('Department', '')).strip(),
            'site': str(row.get('Assigned Site', '')).strip(),
            'project': str(row.get('Project', '')).strip(),
            'nationality': str(row.get('Nationality', '')).strip(),
            'grade': str(row.get('Grade', '')).strip(),
            'activated': False,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        batch.set(doc_ref, payload, merge=True)
        count += 1
        total += 1
        
        if count >= 400:
            batch.commit()
            print(f"Uploaded {total} records...")
            batch = db.batch()
            count = 0
            
    if count > 0:
        batch.commit()
        
    print(f"DONE! {total} employees uploaded to majed-code1 successfully.")

if __name__ == "__main__":
    upload_data()

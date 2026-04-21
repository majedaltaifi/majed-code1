import firebase_admin
from firebase_admin import credentials, firestore, auth
import os

# 1. Setup
cred_path = 'cloude-code1-firebase-adminsdk-fbsvc-60c02c7001.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def sync_employees_to_auth():
    print("Fetching employees from Firestore...")
    docs = db.collection('employees').stream()
    
    count = 0
    errors = 0
    
    for doc in docs:
        data = doc.to_dict()
        email = data.get('email')
        emp_no = data.get('emp_no') or doc.id
        
        if not email or "@" not in email:
            continue
            
        try:
            # Check if user already exists in Auth
            try:
                auth.get_user_by_email(email)
            except auth.UserNotFoundError:
                # Create user in Firebase Auth
                pwd = data.get('password') or f"NIT{emp_no}!"
                auth.create_user(
                    uid=str(emp_no),
                    email=email,
                    password=pwd,
                    display_name=data.get('name') or data.get('name_en')
                )
                count += 1
                if count % 10 == 0:
                    print(f"Synced {count} users to Auth...")
        except Exception as e:
            errors += 1
            
    print(f"COMPLETED! {count} new users added to Firebase Authentication.")
    print(f"Skipped {errors} users due to errors or duplicates.")

if __name__ == "__main__":
    sync_employees_to_auth()

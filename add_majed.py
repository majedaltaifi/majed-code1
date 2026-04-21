import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime

# Initialize Firebase Admin
cred = credentials.Certificate("majed-code1-service-key.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Employee Data
emp_no = "3734"
email = "majedaltaifi1@gmail.com"
employee_data = {
    "branch_code": "KSA",
    "department": "Human Resources and Administration",
    "division": "HRIS",
    "email": email,
    "emp_no": emp_no,
    "grade": "C2",
    "loc_type": "Office",
    "name": "Majed Abdulaziz Ali Altaifi",
    "name_en": "Majed Abdulaziz Ali Altaifi",
    "password": "Nesma1212",
    "phone": "966537244766",
    "position": "HRIS Administrator",
    "project": "Overhead/HR",
    "site": "Jeddah Main Office - Randa Tower",
    "unit": "System Support",
    "updated_at": firestore.SERVER_TIMESTAMP
}

# 1. Add to Firestore
db.collection("employees").document(emp_no).set(employee_data)
print(f"Firestore: Added/Updated {emp_no}")

# 2. Add to Firebase Auth
try:
    user = auth.create_user(
        email=email,
        password=employee_data['password'],
        display_name=employee_data['name'],
        uid=emp_no
    )
    print(f"Auth: Created user {email}")
except Exception as e:
    if 'ALREADY_EXISTS' in str(e) or 'already in use' in str(e).lower():
        print(f"Auth: User {email} already exists.")
    else:
        print(f"Auth: Error creating user: {e}")

print("DONE!")

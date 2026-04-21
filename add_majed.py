import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase Admin
cred = credentials.Certificate("cloude-code1-firebase-adminsdk-fbsvc-60c02c7001.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Employee Data
emp_no = "3734"
employee_data = {
    "branch_code": "KSA",
    "department": "Human Resources and Administration",
    "division": "HRIS",
    "email": "majedaltaifi1@gmail.com",
    "emp_no": emp_no,
    "grade": "C2",
    "loc_type": "Office",
    "name": "Majed Abdulaziz Ali Altaifi",
    "password": "1212",
    "phone": "966537244766",
    "position": "HRIS Administrator",
    "project": "Overhead/HR",
    "site": "Jeddah Main Office - Randa Tower",
    "unit": "System Support",
    "updated_at": firestore.SERVER_TIMESTAMP
}

# Add to Firestore
db.collection("employees").document(emp_no).set(employee_data)

print(f"Successfully added employee: {employee_data['name']} (ID: {emp_no})")

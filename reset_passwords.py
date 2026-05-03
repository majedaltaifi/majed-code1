import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase Admin
cred = credentials.Certificate('majed-code1-service-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

NEW_PASSWORD = "123456"

def reset_all_passwords():
    print("Fetching employees from Firestore...")
    employees_ref = db.collection('employees')
    docs = employees_ref.get()
    
    count = 0
    errors = 0
    
    for doc in docs:
        data = doc.to_dict()
        email = data.get('email')
        emp_id = doc.id
        
        if not email:
            print(f"Skipping {emp_id}: No email found.")
            continue
            
        try:
            # 1. Update/Create in Firebase Auth
            try:
                user = auth.get_user_by_email(email)
                auth.update_user(user.uid, password=NEW_PASSWORD)
                print(f"Updated Auth for: {email}")
            except auth.UserNotFoundError:
                # If user doesn't exist in Auth, we don't necessarily want to create them 
                # unless the app logic requires it. But the user said "make all 123456".
                # Usually they are created on first login in the app.
                # So we just update the Firestore record for now.
                print(f"User not in Auth yet: {email}")
            
            # 2. Update Firestore record
            employees_ref.document(emp_id).update({
                'password': NEW_PASSWORD
            })
            count += 1
            
        except Exception as e:
            print(f"Error updating {email}: {e}")
            errors += 1
            
    print(f"\n--- DONE ---")
    print(f"Successfully updated: {count} employees.")
    print(f"Errors encountered: {errors}")

if __name__ == "__main__":
    reset_all_passwords()

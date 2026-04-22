import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('majed-code1-service-key.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def verify_and_print():
    emp_no = '2838'
    print(f"--- Checking Firestore for node: chats/{emp_no} ---")
    
    chat_doc = db.collection('chats').document(emp_no).get()
    if chat_doc.exists:
        print(f"SUCCESS: Found chat document for {emp_no}")
        print("Metadata:", chat_doc.to_dict())
        
        msgs = db.collection('chats').document(emp_no).collection('messages').get()
        print(f"Found {len(msgs)} messages in 'messages' subcollection:")
        for m in msgs:
            print(f" - [{m.id}] {m.to_dict()}")
    else:
        print(f"ERROR: No chat document found for {emp_no} in 'chats' collection.")
        # List all documents in chats to see what's there
        all_chats = db.collection('chats').get()
        print(f"Total documents in 'chats' collection: {len(all_chats)}")
        for c in all_chats:
            print(f" - Found ID: {c.id}")

if __name__ == "__main__":
    verify_and_print()

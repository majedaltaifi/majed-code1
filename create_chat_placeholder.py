import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('majed-code1-service-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def create_chat_place():
    emp_no = '2838'
    chat_ref = db.collection('chats').document(emp_no)
    
    # Set metadata
    chat_ref.set({
        'senderName': 'Majed (Test)',
        'lastMessage': 'Initial sync message from system',
        'updatedAt': firestore.SERVER_TIMESTAMP
    }, merge=True)
    
    # Add first message
    msg_ref = chat_ref.collection('messages').document('init_msg')
    msg_ref.set({
        'text': 'System link established. You can now send messages from the app.',
        'senderId': 'system',
        'senderName': 'System',
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    
    print(f"Successfully created chat place for employee {emp_no} in collection 'chats'")

if __name__ == "__main__":
    create_chat_place()

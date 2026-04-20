import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# This assumes the user has the credentials file locally or I can use the default app if initialized
# Actually, I'll just use a browser agent to do it via the UI I just built. 
# It's safer because I don't have the service account key.


from google.cloud import firestore

from app.core.config import FIREBASE_PROJECT_ID


# Conectarse al emulador local de Firestore.
db = firestore.Client(project=FIREBASE_PROJECT_ID)


import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env situado en la raíz.
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "FriendlyEats FastAPI")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
FIREBASE_PROJECT_ID = os.getenv(
    "FIREBASE_PROJECT_ID",
    "demo-friendlyeats"
)
FIRESTORE_EMULATOR_HOST = os.getenv(
    "FIRESTORE_EMULATOR_HOST",
    "127.0.0.1:8080"
)

# Indicar al cliente de Google que utilice Firestore local.
os.environ["FIRESTORE_EMULATOR_HOST"] = FIRESTORE_EMULATOR_HOST

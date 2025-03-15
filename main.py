from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import pywhatkit

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["TestDB"]
clc = db["TestInfo"]

print("Connected to MongoDB!")

# Define request model
class MessageRequest(BaseModel):
    message: str  # User provides a message to send

# API Route to send messages
@app.post("/send-messages")
def send_messages(data: MessageRequest):
    try:
        name_list = []
        number_list = []

        # Fetch all contacts from MongoDB
        for doc in clc.find():
            name_list.append(doc['name'])
            number_list.append(doc['contact'])

        # Send message to each contact
        for i in range(len(name_list)):
            pywhatkit.sendwhatmsg_instantly(number_list[i], data.message, 10, True, 2)

        return {"status": "Success", "message": "Messages sent successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root Route
@app.get("/")
def home():
    return {"message": "FastAPI WhatsApp Bot is running!"}



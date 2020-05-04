from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bson.json_util import dumps
import re
from errorHandler import errorHandler, Error404
import nltk
from bson import ObjectId
from config import DBURL
from app import *
nltk.download('vader_lexicon')
nltk.download('stopwords')


client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
db = client.get_default_database()
users = db["users"]
chats = db["chats"]

#GET user_id
def getUserid(user_id):
    userId = re.compile(f"^{user_id}", re.IGNORECASE)
    uid = users.find_one({"_id":ObjectId(userId)})
    if not uid:
        print("ERROR")
        raise Error404("user_id not found")
    return {
        "status":"success",
        "dbresponse":dumps(uid)
    }
#GET chat_id
def getChatid(chat_id):
    chatId = re.compile(f"^{chat_id}", re.IGNORECASE)
    cid = chats.find_one({"_id":ObjectId(chatId)})
    if not cid:
        print("ERROR")
        raise Error404("chad_id not found")
    print("OK")
    return {
        "status":"success",
        "dbresponse":dumps(cid)
    }
    
    
### 1. User endpoints

#GET create user @return user_id
def createUser(username):
    user = {"name":username} 
    userID = users.insert_one(user)
    return str(userID.inserted_id)

### 2. Chat endpoints

#GET  Create a conversation to load messages 
#**Params:** An array of users ids `[user_id]`
def chatCreator(user_id):
    user=user_id.split(",") #array
    chat = chats.insert_one({"Users": user,"Messages": []})
    return str(chat.inserted_id)
    
#GET Add a user to a chat
def addUser(chat_id,user_id):
    chatID = chats.find_one({"_id": ObjectId(chat_id)})
    if not chatID:
        print("ERROR")
        raise Error404("chad_id not found")
    else:  
        chat = chats.update_one({"_id": ObjectId(chat_id)},{"$addToSet":{"Users": user_id}})
        return "User added"
    


#POST Add a message to the conversation @return messageID
def addmessage(chat_id,user_id,text):
    user = users.find_one({"_id": ObjectId(user_id)})
    chatID = chats.find_one({"_id": ObjectId(chat_id)})
    if chatID and user:
        messageID =ObjectId()
        message = chats.update_one({"_id": ObjectId(chat_id)},{"$addToSet":{"Messages": {"message_id": messageID ,"Users": user_id, "text":text}}})
        return str(messageID)
    else:
        return "ERROR: Chat or user cannot be found"

#GET Get all mesages from "chat_id"@return  json array with all messages from this `chat_id`
def getallmessages(chat_id):
    allmessages= chats.find({"_id": ObjectId(chat_id)},{"_id":0,"Messages":1})
    return dumps(allmessages) #return json array
    
#GET all sentiments from messages in the chat @return json with all sentiments from messages in the chat
def sentiments(chat_id):
    sentimentAnalyzer = SentimentIntensityAnalyzer()
    sentiment = list(chats.find({"_id": ObjectId(chat_id)},{"_id":0,"Messages":1}))
    sentiment= sentiment[0]
    messages = sentiment["Messages"] 
    sentimentGetText=[]
    for e in messages:
        sentimentGetText.append(e["text"])
    sentimentGetText=" ".join(sentimentGetText) #Lo paso todo a string para analizar el sentimiento
    
    return dumps(sentimentAnalyzer.polarity_scores(sentimentGetText))#return json

### 3. User recomendation
#GET recommend friend 
def recommend(user_id):

    #text =chats.find({},{"text":1})
    #x =[e for e in text] #chatId donde hay mensajes
    #x2 =x[0]
    #idtext = chats.find(x2,{"text":1})
    
        
    return ""



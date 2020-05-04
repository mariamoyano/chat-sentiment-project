from app import *
from errorHandler import errorHandler, Error404
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from endpoints import *
from config import PORT


#API help
@app.route("/help")
def index():
    pagetitle = "Chat Sentiment Analysis Service"
    return render_template("index.html",mytitle=pagetitle,mycontent="WELCOME!!!")

@app.route("/")
def help():
    return "Hello. Please, enter /help to get help."

@app.route("/user/<user_id>")
@errorHandler
def getUserID(user_id):
    return getUserid(user_id)

@app.route("/chat/<chat_id>")
@errorHandler
def getID(chat_id):
    return getUserid(chat_id)

### 1. User endpoints
#GET create user
@app.route('/user/create/<username>')
@errorHandler
def createUserName(username):
    return createUser(username)

#GET recommend friend
@app.route("/user/<user_id>/recommend")
@errorHandler
def recommendFriend(user_id):
    return recommend(user_id)

### 2. Chat endpoints

#GET  Create a conversation to load messages
@app.route('/chat/create')
@errorHandler
def chatCreate():
    user_id = request.args.get("users")
    return chatCreator(user_id)

#GET Add a user to a chat
@app.route('/chat/<chat_id>/adduser')
@errorHandler
def addUserTo(chat_id):
    user_id = request.args.get("users")
    return addUser(chat_id,user_id)

#POST Add a message to the conversation
@app.route("/chat/<chat_id>/addmessage")
@errorHandler
def addMessage(chat_id):
    user_id = request.args.get("users")
    text = request.args.get("message")
    return addmessage(chat_id,user_id,text)

#GET Get all mesages from "chat_id"
@app.route("/chat/<chat_id>/list")
@errorHandler
def getAllMessages(chat_id):
    return getallmessages(chat_id)

#GET all sentiments from messages in the chat
@app.route("/chat/<chat_id>/sentiment")
@errorHandler
def sentimentAnalysis(chat_id):
    return sentiments(chat_id)



                            
app.run("0.0.0.0", PORT, debug=True)
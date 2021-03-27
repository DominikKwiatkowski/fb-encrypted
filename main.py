import fbchat
from Conversation import Conversation
from threading import Thread
import asyncio
import time

from Listener import Listener


def fetcher(client: fbchat.Client):
    users = client.fetch_users()

    print("users' IDs: {}".format([user.id for user in users]))
    print("users' names: {}".format([user.name for user in users]))

    return users

def fbtest():
    email = "dom.kwiatek@wp.pl"
    password = "dom.Kwiatek1"
    session = fbchat.Session.login(email, password)
    client = fbchat.Client(session=session)
    users = fetcher(client)
    conversations = []
    for user in users:
        conversations.append(Conversation(user))
    listener = Listener(conversations, session)
    listener.start()
    input()
    print("Own id: {}".format(session.user.id))
    conversation = conversations[0]
    conversation.changeEncryption()
    time.sleep(5)
    while True:
        message = input()
        if message == "change":
            conversation.changeEncryption()
            time.sleep(5)
        conversation.messagesToSent.append(message)
        conversation.sendMessages()

    session.logout()
#print("Podaj email")
#email = input()
#print("podaj haslo")
#password = input()

def test(conversation, conversation1):
    conversation.changeEncryption()
    conversation1.handleNewMessages()
    conversation.handleNewMessages()
    conversation1.handleNewMessages()
    conversation.handleNewMessages()

    conversation1.changeEncryption()
    conversation.handleNewMessages()
    conversation1.handleNewMessages()
    conversation.handleNewMessages()
    conversation1.handleNewMessages()

    conversation.messagesToSent.append("Ala ma kota")
    conversation.messagesToSent.append("Dominik kocha Ole")
    conversation.sendMessages()
    conversation1.handleNewMessages()


def test1(conversation, conversation1):
    conversation.changeEncryption()
    conversation1.handleNewMessages()
    conversation.handleNewMessages()
    conversation1.handleNewMessages()
    conversation.handleNewMessages()

    conversation1.changeEncryption()
    conversation.handleNewMessages()
    conversation1.handleNewMessages()
    conversation.handleNewMessages()
    conversation1.handleNewMessages()

    conversation.messagesToSent.append("Ala ma kota")
    conversation.messagesToSent.append("Dominik kocha Ole")
    conversation.sendMessages()
    conversation1.handleNewMessages()



#conversation = Conversation(1)
#conversation1 = Conversation(conversation)
#conversation.user = conversation1
#test(conversation, conversation1)
#test1(conversation, conversation1)
fbtest()

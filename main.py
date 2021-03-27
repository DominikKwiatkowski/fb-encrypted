import fbchat
from Conversation import Conversation
from threading import Thread
import asyncio
import time
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
    listener = fbchat.Listener(session=session, chat_on=False, foreground=False)
    print("Own id: {}".format(session.user.id))
    for event in listener.listen():
        if isinstance(event, fbchat.MessageEvent):
            print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
            if event.author.id != session.user.id:
                text = input()
                event.author.send_text(text)
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


conversation = Conversation(1)
conversation1 = Conversation(conversation)
conversation.user = conversation1
test(conversation, conversation1)
test1(conversation, conversation1)
#fbtest()

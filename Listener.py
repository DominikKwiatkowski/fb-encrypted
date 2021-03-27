import time

import fbchat
from Conversation import Conversation
import threading

class Listener(threading.Thread):


    def __init__(self, conversations, session):
        threading.Thread.__init__(self)
        self.conversations = conversations
        self.session = session

    def run(self):
        listener = fbchat.Listener(session=self.session, chat_on=False, foreground=False)
        for event in listener.listen():
            if isinstance(event, fbchat.MessageEvent):
                if event.author.id != self.session.user.id:
                    for conversation in self.conversations:
                        if event.author.id == conversation.user.id:
                            if conversation.convMode == 1:
                                message = event.message.text.split(",")
                            else:
                                message = ["","",event.message.text,""]
                            while not conversation.mutex.acquire():
                                time.sleep(0.001)
                            conversation.newMessages.append(message)
                            conversation.mutex.release()

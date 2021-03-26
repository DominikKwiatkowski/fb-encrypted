import os
import threading
import rsa
import fbchat
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time


# s/mine check
# as-128
class Conversation(threading.Thread):

    def __init__(self, user):
        threading.Thread.__init__(self)
        self.myKey = 1
        self.myPubKey = 1
        self.convKey = 1
        self.mySign = 1
        self.myPubSign = 1
        self.convSign = 1
        self.messages = []
        self.user = user
        self.newMessages = []
        self.messagesToSent = []
        # 0 - non-encrypted 1 - encrypted
        self.myMode = 0
        self.convMode = 0

    def generateKey(self):
        (myPubKey, myKey) = rsa.newkeys(1024)
        (myPubSign, mySign) = rsa.newkeys(1024)
        return myPubKey, myKey, myPubSign, mySign

    def decode(self, key, signature, message, iv):
        if self.myMode and self.convMode:
            key = bytes.fromhex(key)
            signature = bytes.fromhex(signature)
            message = bytes.fromhex(message)
            iv = bytes.fromhex(iv)
            if rsa.verify(key, signature, self.convSign):
                key = rsa.decrypt(key, self.myKey)
                iv = rsa.decrypt(iv, self.myKey)
                aes_dec = AES.new(key, AES.MODE_CBC, iv)
                message = unpad(aes_dec.decrypt(message),AES.block_size)
                return message.decode('UTF-8')
            else:
                print("Verification failed")
        else:
            return message

    def encrypt(self, message: str):
        if self.myMode and self.convMode:
            message = message.encode('UTF-8')
            key = os.urandom(16)
            aes_enc = AES.new(key, AES.MODE_CBC)
            encrypted_key = rsa.encrypt(key, self.convKey)
            encrypted_message = aes_enc.encrypt(pad(message, AES.block_size)).hex()
            return encrypted_key.hex(), rsa.sign(encrypted_key, self.mySign, "SHA-1").hex(), encrypted_message, \
                rsa.encrypt(aes_enc.iv, self.convKey).hex()
        else:
            return "", "", message,""

    def sendMessages(self):
        for message in self.messagesToSent:
            key, signature, message, iv = self.encrypt(message)

            self.user.newMessages.append([key, signature, message, iv])
        self.messagesToSent = []

    def handleNewMessages(self):
        for message in self.newMessages:
            message = self.decode(message[0], message[1], message[2], message[3])
            if message.startswith("New sign"):
                message = message[len("New sign"):]
                self.messagesToSent.append("@cceptedSign")
                self.convSign = rsa.PublicKey.load_pkcs1(message.encode(encoding="latin-1"), 'DER')
                self.sendMessages()
            elif message.startswith("New key"):
                message = message[len("New key"):]
                self.messagesToSent.append("@cceptedKey")
                self.convKey = rsa.PublicKey.load_pkcs1(message.encode(encoding="latin-1"), 'DER')
                self.sendMessages()
                self.convMode = 1
            else:
                print(message)
        self.newMessages = []

    def changeEncryption(self):
        myPubKey, myKey, myPubSign, mySign = self.generateKey()
        self.messagesToSent.append("New sign" + str(myPubSign.save_pkcs1('DER'), encoding="latin-1"))
        self.sendMessages()
        time.sleep(3)
        # send my pub sign
        for message in self.newMessages:
            message = self.decode(message[0], message[1], message[2],message[3])
            if message == "@cceptedSign":
                self.mySign = mySign
                self.myPubSign = myPubSign
                self.messagesToSent.append("New key" + str(myPubKey.save_pkcs1('DER'), encoding="latin-1"))
                self.sendMessages()
                time.sleep(3)
                for message1 in self.newMessages:
                    message1 = self.decode(message1[0], message1[1], message1[2],message1[3])
                    if message1 == "@cceptedKey":
                        self.myKey = myKey
                        self.myPubKey = myPubKey
                        self.myMode = 1
                        break
                break
        self.newMessages = []
        return self.myMode

    def run(self):
        time.sleep(1.5)
        self.handleNewMessages()
        time.sleep(3)
        self.handleNewMessages()

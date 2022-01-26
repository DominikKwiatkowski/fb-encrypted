import os
import sys
import threading
import rsa
import fbchat
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time


# s/mine check
# as-128
class Conversation:

    def __init__(self, user):
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
        self.myTmpKey = 1
        self.myTmpPubKey = 1
        self.myTmpSign = 1
        self.myTmpPubSign = 1
        self.mutex = threading.Lock()

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
            try:
                if rsa.verify(key + message + iv, signature, self.convSign):
                    key = rsa.decrypt(key, self.myKey)
                    iv = rsa.decrypt(iv, self.myKey)
                    aes_dec = AES.new(key, AES.MODE_CBC, iv)
                    message = unpad(aes_dec.decrypt(message),AES.block_size)
                    return message.decode('UTF-8')
            except:
                print(sys.exc_info()[0])
            return ""

        else:
            return message

    def encrypt(self, message: str):
        if self.myMode and self.convMode:
            message = message.encode('UTF-8')
            key = os.urandom(16)
            aes_enc = AES.new(key, AES.MODE_CBC)
            encrypted_key = rsa.encrypt(key, self.convKey)
            encrypted_message = aes_enc.encrypt(pad(message, AES.block_size))
            encrypted_iv = rsa.encrypt(aes_enc.iv, self.convKey)
            return encrypted_key.hex(), rsa.sign(encrypted_key + encrypted_message + encrypted_iv, self.mySign, "SHA-1").hex(), encrypted_message.hex(), \
                encrypted_iv.hex()
        else:
            return "", "", message,""

    def sendMessages(self):
        for message in self.messagesToSent:
            key, signature, message, iv = self.encrypt(message)
            if self.myMode == 1:
                self.user.send_text(",".join([key, signature, message, iv]))
            else:
                self.user.send_text(message)
        self.messagesToSent = []

    def handleNewMessages(self):
        while not self.mutex.acquire():
            time.sleep(0.001)
        for message in self.newMessages:
            message = self.decode(message[0], message[1], message[2], message[3])
            if message.startswith("New sign"):
                message = message[len("New sign"):]
                self.messagesToSent.append("@cceptedSign")
                self.sendMessages()
                self.convSign = rsa.PublicKey.load_pkcs1(bytes.fromhex(message), 'DER')

            elif message.startswith("New key"):
                message = message[len("New key"):]
                self.messagesToSent.append("@cceptedKey")
                self.sendMessages()
                self.convKey = rsa.PublicKey.load_pkcs1(bytes.fromhex(message), 'DER')

                self.convMode = 1
            elif message.startswith("@cceptedSign"):
                self.changeEncryptionSign()
            elif message.startswith("@cceptedKey"):
                self.changeEncryptionKey()
            else:
                print(message)
        self.newMessages = []
        self.mutex.release()

    def changeEncryption(self):
        self.myTmpPubKey, self.myTmpKey, self.myTmpPubSign, self.myTmpSign = self.generateKey()
        self.messagesToSent.append("New sign" + self.myTmpPubSign.save_pkcs1('DER').hex())
        self.sendMessages()


    def changeEncryptionSign(self):
        self.mySign = self.myTmpSign
        self.myPubSign = self.myTmpPubSign
        self.messagesToSent.append("New key" + self.myTmpPubKey.save_pkcs1('DER').hex())
        self.sendMessages()

    def changeEncryptionKey(self):
        self.myKey = self.myTmpKey
        self.myPubKey = self.myTmpPubKey
        self.myMode = 1

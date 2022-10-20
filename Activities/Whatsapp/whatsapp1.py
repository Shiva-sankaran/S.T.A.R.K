import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message

driver = WhatsAPIDriver(profile = '/home/shivasankaran/S.T.A.R.K/Activities/Whatsapp/profile',loadstyles = True)
t = input()
time.sleep(10)
while True:
    time.sleep(3)
    print("Checking for more messages")
    for contact in driver.get_unread():
        for message in contact.messages:
            if isinstance(message, Message):  # Currently works for text messages only.
                contact.chat.send_message(message.content)
import imaplib
import email
from dotenv import dotenv_values
import os
import datetime

now = datetime.datetime.now() + datetime.timedelta(hours=2)
print(now.strftime("[%d-%m-%Y %H:%M:%S]")+ " Script is running")

config = dotenv_values(".env")
password = config['KEY']
email_address = config['email']

imap_server = "imap.gmail.com"

imap = imaplib.IMAP4_SSL("74.125.20.108")
imap.login(email_address,password)

imap.select('Inbox')

status, msgnums = imap.search(None, 'TO "bitcoin-dev@lists.linuxfoundation.org"')

for msgnum in msgnums[0].split():
    
    _, data = imap.fetch(msgnum, "(RFC822)")
    message = email.message_from_bytes(data[0][1])
    subject = message.get("Subject")
    
    subject = subject.replace(',','')
    parts = subject.split(' ')
    vol = parts[3]
    subject = subject.replace(' ','_')
    
    folder = f'bitcoin-dev_Digest_Vol_{vol}'
    path = f'{folder}/{subject}.md'
    
    if os.path.exists(folder):
      if os.path.exists(path):
        pass
      else :
        with open(path,'w') as f :
          f.write(message.get_payload())
        print(f"Le bitcoin-dev Digest {subject} a été ajouté aux fichiers dans {folder}")

    else :
        os.mkdir(folder)
        with open(path,'w') as f:
          f.write(message.get_payload())
        print(f"Le bitcoin-dev Digest {subject} a été ajouté aux fichiers dans {folder}")

now = datetime.datetime.now() + datetime.timedelta(hours=2)
print(now.strftime("[%d-%m-%Y %H:%M:%S]")+ " Script is finished")

imap.close()
imap.logout()


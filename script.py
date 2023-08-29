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
    # parts = ['bitcoin-dev', 'Digest', 'Vol', 'xx', 'Issue', 'yy']
    vol = parts[3]
    # volume number
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

# Search for digest email
#subject = 'bitcoin-dev Digest, Vol 96, Issue 46'
#status, data = imap.search(None, f'SUBJECT "{subject}"')
#subject = subject.replace(',','')
#subject = subject.replace(' ','_')
#
#for num in data[0].split():
#    status, data = imap.fetch(num, '(RFC822)')
#    email_msg = email.message_from_bytes(data[0][1])
#    # Split subject on '_' 
#    parts = subject.split('_')
#    print(parts)
#    # Parts is now ['bitcoin-dev', 'Digest', 'Vol', 96', 'Issue', '46']
#
#    # Get the element containing the volume  
#    vol = parts[3]
#    print(vol)
#
#    # Construct folder path 
#    folder = f'bitcoin-dev_Digest_Vol_{vol}'
#    path = f'{folder}/{subject}.md'
#
#    # Create folder if it doesn't exist
#    if not os.path.exists(folder):
#        os.mkdir(folder)
#
#    # Save email content to file
#    with open(path, 'w') as f:
#        f.write(email_msg.get_payload())
#
# Close connection  
imap.close()
imap.logout()

#
#
#print(msgnums)
#
#msgnum =msgnums[0].split()[0]
#_, data = imap.fetch(msgnum,'(RFC822)')
#message = email.message_from_bytes(data[0][1])
#subject = message.get("Subject")
#subject = subject.replace(',','')
#subject = subject.replace(' ','_')
#print(subject)
##print(message)
#
#

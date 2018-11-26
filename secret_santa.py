import smtplib
import time
import imaplib
import email
import getpass
import poplib
import logging
import string
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.parser import BytesParser


imap_host = 'imap.gmail.com'
imap_user = 'secretsantasuhboi@gmail.com'
imap_pass = 'HEYTHEREDAWG'

imap = imaplib.IMAP4_SSL(imap_host)

imap.login(imap_user, imap_pass)

print('Logged In!')

status, info = imap.select()

status, msg_ids = imap.search(None, 'ALL')
email_dict = {}
for num in msg_ids[0].split():
    status, msg = imap.fetch(num, '(RFC822)')
    the_string = str(msg[0][1])

    #print (the_string)
    #print()

    from_addr = the_string[the_string.find('From:'):]
    from_name = from_addr[from_addr.find(' ') + 1: from_addr.find('<') - 1]
    from_addr = from_addr[from_addr.find('<') + 1:from_addr.find('>')]
    
    subject_line = the_string[the_string.find('Subject:'):]
    subject_line = subject_line[subject_line.find(' ') + 1:subject_line.find('\\r\\n')]
    #print(from_name, from_addr, subject_line)
    
    the_string = the_string[the_string.find('Inbound message'):]
    the_string = the_string[len('Inbound message\r\nX-Antivirus-Status: Clean\r\n\r\n--') + 4:the_string.find('Content-Type: text/html')]

    if(the_string.find('charset="UTF-8"') != -1):
        the_string = the_string[the_string.find('charset="UTF-8"'):]
        the_string = the_string[len('charset="UTF-8"') + 8:]
        
    the_string = the_string[:the_string.find('\\r\\n\\r\\n--')]
    #print(str(the_string))
    if(subject_line == 'Secret Santa List'):
        email_dict[from_name] = (from_addr, the_string)
    #print()

#print(email_dict)

assignment_dict = {}
while True:
    special = False
    potential_candidates = list(email_dict.keys())
    for person in email_dict.keys():
        print(person, potential_candidates)
        potential_candidate = ''
        index = 0
        while True:
            index = random.randint(0, len(potential_candidates) - 1)
            potential_candidate = potential_candidates[index]
            if(potential_candidate != person):
                break
            if(potential_candidate == person and len(potential_candidates) == 1):
                special = True
                break
        potential_candidates.pop(index)
        assignment_dict[person] = potential_candidate
    if not special:
        break
    print()
    print('SPECIAL HAS BEEN HIT')
    print()

print(assignment_dict)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()

server.login(imap_user, imap_pass)

for person in assignment_dict.keys():
    msg = MIMEMultipart()
    recipient = assignment_dict[person]
    recipient_email = email_dict[recipient][0]
    recipient_message = email_dict[recipient][1]
    msg['From'] = imap_user
    msg['To'] = 'dhruvdeepu@gmail.com'
    msg['Subject'] = 'HOI'
    real_msg = person + ' was assigned ' + recipient + ' recipient wants:\n' 
    for text in recipient_message.split('\\r\\n')[1:]:
        real_msg += text + '\r\n'
    
    msg.attach(MIMEText(real_msg, 'plain'))
    server.send_message(msg)
    
print(assignment_dict)


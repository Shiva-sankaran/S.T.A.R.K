import smtplib, ssl,keyring
import imaplib
from itertools import chain
import email
import os
import config as cfg
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def search_string(criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items()))
    return '(%s)' % ' '.join(chain(*c))
def get_body(mail_str):
    if mail_str.is_multipart():
        for payload in mail_str.walk():
            if payload.get_content_type() == "text/plain":
                return(payload.get_payload())
    else:
        return(mail_str.get_payload())
def get_attachment(mail_str):
    if mail_str.is_multipart():
        for payload in mail_str.walk():
            if payload.get("Content-Disposition") is not None:
                print("attachment detected")
                filename = payload.get_filename()
                filepath = os.path.join(cfg.path['receiving'],filename)
                t_dict['attachments'] = filename
                file_data = payload.get_payload(decode = 1)
                if not os.path.exists(filepath):
                    f = open(filepath,'wb')
                    f.write(file_data)
                    print("file downloaded")
                    f.close()

                else:
                    print("file already exsists")


def send_mail(message_dict):
    port = 465  # For SSL
    message = MIMEMultipart()
    message["From"] = cfg.email[message_dict['From_type']]
    message['Subject'] = message_dict['Subject']
    message["To"] = message_dict['To']
    message["cc"] = message_dict["cc"]
    message.attach(MIMEText(message_dict["Body"], "plain"))
    smtp_server = "smtp.gmail.com"
    password = keyring.get_password("email-"+message_dict['From_type'], message["From"])
    
    for filename in message_dict['attachments']:
        a_attachment_path = os.path.join(cfg.path['sending'],filename)
        with open(a_attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(a_attachment_path)}",
            )

        # Add attachment to message and convert message to string
        message.attach(part)
    text_message = message.as_string()
    context = ssl.create_default_context()
    print(message['To']+','+message['cc'])
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(message["From"], password)
        server.sendmail(message["From"], message["To"].split(",") + message["cc"].split(","), text_message)
def search_mail(**kwargs):
    p_criteria = {}
    passing_ids = []
    search_results = []
    for key,value in kwargs.items():
        if value != 'NA':
            p_criteria[key] = value
    del p_criteria['mail_type']

    if "SUBJECT" in p_criteria.keys():
        del p_criteria['SUBJECT']
    if "BODY" in p_criteria.keys():
        del p_criteria['BODY'] 
    query_string = search_string(p_criteria)
    
    imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
    imap_ssl_port = 993
    mailaddr = cfg.email[kwargs['mail_type']]
    password = keyring.get_password("email-"+kwargs['mail_type'], mailaddr)
    imap = imaplib.IMAP4_SSL(imap_ssl_host)
    imap.login(mailaddr, password)
    imap.select('Inbox')
    status , m_ids_data = imap.search(None, query_string)# BEFORE "01-Jan-2020" SINCE "01-Jan-2015")')
    for m_id in m_ids_data[0].split()[::-1]:
        status , m_data = imap.fetch(m_id, '(RFC822)')
        m_as_bytes = m_data[0][1]
        result_mail = email.message_from_bytes(m_as_bytes)
        print(type(result_mail["subject"]))
        if ( kwargs['SUBJECT'] == 'NA' or kwargs['SUBJECT'] in result_mail["subject"]) and (kwargs["BODY"] == 'NA' or kwargs["BODY"] in get_body(result_mail) ):
            passing_ids.append(m_id)           
    print(passing_ids,"&&&")
    for p_id in passing_ids:
        t_dict = {}
        status , m_data = imap.fetch(p_id, '(RFC822)')
        m_as_bytes = m_data[0][1]
        result_mail = email.message_from_bytes(m_as_bytes)
        t_dict['id'] = p_id
        t_dict["sender"] = result_mail['from']
        t_dict["subject"] = result_mail["subject"]
        t_dict["r_date"] = result_mail['date']
        t_dict['body'] = get_body(result_mail)
        t_dict['attachments'] = get_attachment(result_mail)
        search_results.append(t_dict)
    print("search completed succesully found %d results"%len(search_results))
    print(search_results)


import smtplib, ssl,keyring
import imaplib
import email
import os
import config as cfg
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_mail(message_dict):
    port = 465  # For SSL
    message = MIMEMultipart()
    message["From"] = cfg.email[message_dict['From_type']]
    message['Subject'] = message_dict['Subject']
    message["To"] = message_dict['To']
    message["cc"] = ""
    if "cc" in message_dict.keys():
        message["cc"] = message_dict["cc"]
    message.attach(MIMEText(message_dict["Body"], "plain"))
    smtp_server = "smtp.gmail.com"
    password = keyring.get_password("email-"+message_dict['From_type'], message["From"])
    if "attachments" in message_dict.keys():
        for filename in message_dict['attachments']:
            a_attachment_path = os.path.join(cfg.paths['sending'],filename)
            with open(a_attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(a_attachment_path)}",
                    )
                message.attach(part)

    text_message = message.as_string()
    context = ssl.create_default_context()
    print(message['To']+','+message['cc'])
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(message["From"], password)
        server.sendmail(message["From"], message["To"].split(",") + message["cc"].split(","), text_message)
def search_mail(**kwargs):
    download_path = cfg.paths("receiving")
    result_mail_details = {}
    imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
    imap_ssl_port = 993
    mailaddr = cfg.email[kwargs['From_type']]
    password = keyring.get_password("email-"+kwargs['From_type'], mailaddr)
    imap = imaplib.IMAP4_SSL(imap_ssl_host)
    imap.login(mailaddr, password)
    imap.select('Inbox')
    status , m_ids_data = imap.search(None, 'FROM "vp.shivasan@iitgn.ac.in"')
    for m_id in m_ids_data[0].split()[::-1]:
        status , m_data = imap.fetch(m_id, '(RFC822)')
        m_as_bytes = m_data[0][1]
        result_mail = email.message_from_bytes(m_as_bytes)
        print(result_mail)
        result_mail_details["sender"] = result_mail['from']
        result_mail_details["subject"] = result_mail["subject"]
        result_mail_details["r_date"] = result_mail['date']
        if result_mail.is_multipart():
            for payload in result_mail.walk():
                print(payload.get_content_type(),"!!!!12")
                if payload.get_content_type() == "text/plain":
                    result_mail_details['body'] = payload.get_payload()
                if payload.get("Content-Disposition") is not None:
                    print("!!!!!!!!!")
                    filename = payload.get_filename()
                    filepath = os.path.join(download_path,filename)
                    result_mail_details['attachments'] = filename
                    file_data = payload.get_payload(decode = 1)
                    if not os.path.exists(filepath):
                        f = open(filepath,'wb')
                        f.write(file_data)
                        print("file downloaded")
                        f.close()

                    else:
                        print("file already exsists")

            print(result_mail_details)
        break

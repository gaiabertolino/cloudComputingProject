from email import encoders
from email.mime.base import MIMEBase
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


# Connecting to the account


def send_email(user, pwd, recipient, subject, fileToSend, body):
    body = body
    FROM = user
    TO = recipient #if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = SUBJECT

    msgText = MIMEText(body, 'plain')
    msg.attach(msgText)

    # Attach the file
    if fileToSend != "":
        file = fileToSend
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(open(file, 'rb').read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(attachment)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        message = msg.as_string()
        server.sendmail(FROM, TO, message)
        server.close()
        print('Successfully sent the mail')
    except:
        print("Failed to send mail")


import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_gmail(reciver_email,reciver_name):
    verification_code = random.randint(100000,999999)
    mail_content = f"""
    <html>
    <h2>Dear {reciver_name},</h2>
    <body>
    <font size=05>
    <p style="color:#000AFA">
    You have chosen the best way to apply and find fund and best professors that suit for you,
    .<br> We are sure that is not going to be easy, however it will have the sweetest results
    <br>
    <br>
    </p>

    <b style="color:#00FF00"> your activation code is: {verification_code}</b>
    </font>
    </body>
    </html>
     """
    
    #The mail addresses and password
    sender_address = 'apply4fund@gmail.com'
    sender_pass = 'glcrtwnsthfjrtfo'
    receiver_address = reciver_email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Verification code'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    return verification_code

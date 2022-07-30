import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd


def send_forgotten_password(reciver_email,reciver_name):

    df = pd.read_excel('db_streamlit.xlsx',index_col=0)
    user_ind = df.loc[df.email_address == reciver_email].index
    pass_user = df.at[user_ind[0],'password'] 

    mail_content = f"""
    <html>
    <h3>Dear {reciver_name}</h3>,
    <body>
    <font size=04>
    Hope this message finds you well,

    We have recivied a request indicating that you have forgotten you password.<br>
    As a reminder we can mention that your password is: <b>{pass_user}</b>
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
    message['Subject'] = 'Forgotten Password'   #The subject line
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
    return pass_user

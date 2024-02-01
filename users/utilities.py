from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = settings.EMAIL_HOST_USER
sender_password = settings.EMAIL_HOST_PASSWORD

def send_message(first_name, last_name, receipient_email, access_token,name):
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receipient_email
        message['Subject']  = "Invitation to Share History and Love."
        
        body = f"""Hey {name},
{last_name} {first_name} has invited you to share their lovely moments with you on 'PHOTIE' an online photo gallery, please use your email and the access_token below to access them.
                        {access_token}
Please visit:

PHOTIE TEAM🎊\n
        """
        message.attach(MIMEText(body, "plain"))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        server.login(sender_email,sender_password)
        
        server.sendmail(sender_email, receipient_email, message.as_string())
        
        server.quit()
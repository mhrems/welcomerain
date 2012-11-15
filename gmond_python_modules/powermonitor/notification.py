'''
Created on Sep 26, 2012

@author: bond
'''
import cont
import smtplib
from email.mime.text import MIMEText

class Notification():
    pass

class EmailNotification(Notification):
    
    def __init__(self):
        self.smtpUser = cont.NOTI_SMTP_EMAIL
        self.smtpPass = cont.NOTI_SMTP_PASS
        self.fromEmail = cont.NOTI_FROM_EMAIL
        self.toEmail = cont.NOTI_TO_EMAIL

    
    def getSmtpserver(self):
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(self.smtpUser, self.smtpPass)
        return smtpserver
    
    def getEmailMessage(self,sMessage):
        msg = MIMEText(sMessage)
        msg['Subject'] = cont.EMAIL_TITLE
        msg['From'] = self.fromEmail
        msg['To'] = self.toEmail
        return msg.as_string()
        
    def sendEmail(self,sMessage):
        smtpserver = self.getSmtpserver()
        emailMsg = self.getEmailMessage(sMessage)
        smtpserver.sendmail(self.fromEmail, [self.toEmail], emailMsg)
        smtpserver.quit()
        

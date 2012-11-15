

import smtplib
from email.mime.text import MIMEText
import urllib
import urllib2


class Notification():
    
    def sendEmailNotification(self,fromEmail,toEmail,sTitle,sMessage):
        cEmailNotification = EmailNotification()
        cEmailNotification.sendEmail(fromEmail,toEmail,sTitle,sMessage)
    
    def SendServerNotification(self,userId,serverId,serverIp,alertId,pluginId,alertMessage):
        cServerNotification = ServerNotification()
        cServerNotification.sendApi(userId,serverId,serverIp,alertId,pluginId,alertMessage)

class ServerNotification():
    
    def __init__(self):
        self.apiUrl = 'http://192.168.0.220:8080/api/addAlertHistory/'

    def sendApi(self,userId,serverId,serverIp,alertId,pluginId,alertMessage):
        oPostData = {
            "userId" : userId,
            "serverId" : serverId, 
            "serverIp" : serverIp,
            "alertId" : alertId,
            "pluginId" : pluginId,
            "alertMessage" : alertMessage,
        }
        data = urllib.urlencode(oPostData)         
        request = urllib2.Request(self.apiUrl, data)
        response = urllib2.urlopen(request)
    
class EmailNotification():

    def __init__(self):
        self.smtpUser = 'mhr.noti@gmail.com'
        self.smtpPass = 'vkdnjapdlf'

    def getSmtpserver(self):
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(self.smtpUser, self.smtpPass)
        return smtpserver
    
    def getEmailMessage(self,fromEmail,toEmail,sTitle,sMessage):
        msg = MIMEText(sMessage)
        msg['Subject'] = sTitle
        msg['From'] = fromEmail
        msg['To'] = toEmail
        return msg.as_string()
        
    def sendEmail(self,fromEmail,toEmail,sTitle,sMessage):
        smtpserver = self.getSmtpserver()
        emailMsg = self.getEmailMessage(fromEmail,toEmail,sTitle,sMessage)
        smtpserver.sendmail(fromEmail, [toEmail], emailMsg)
        smtpserver.quit()

cNotification = Notification()
#cNotification.sendEmailNotification('mhr.bond@gmail.com','mhr.bond@gmail.com','test')
#cNotification.SendServerNotification('1','28','192.168.0.2','1','1','alert_message')



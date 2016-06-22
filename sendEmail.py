#encoding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication  
import random as rd
import pdb
import time


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def sendEmail(receivers,subject,message,trials):
    #receivers: a list of strings, stores the email addresses of the receivers.
    #subject: a string, stores the subject of the email.
    #message: a string, stores the plain text of the email.
    #trials: one integer number. program will auto retry until the email is sent or the number of retrials exceeds this number.
    sender = 'shinsyzgz@sohu.com'

    #msgString=('From: %s\n\nTo: %s\n\n\n'%(sender, ','.join(receivers)))
    msgString=''

    msgString=msgString+ '\n'+message

    message = MIMEText(msgString, 'plain', 'utf-8')
    message['From'] = "Guangzhi ZHANG<%s>"%(sender)
    message['To'] = "%s"%(','.join(receivers))


    message['Subject'] = subject

    host="smtp.sohu.com"
    user="shinsyzgz@sohu.com"
    pwd="881028zgz"
    sent=False
    count=0
    while not sent:
        count=count+1
        if count>trials:
            print 'ERROR: FAILED TO SEND EMAIL.'
            break
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(host,25)
            smtpObj.login(user,pwd)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print "result sent to",receivers 
            sent=True
            smtpObj.close()
        except :
            print "sth. wrong when sending email. retrying no.", count
            sent=False
            smtpObj.close()
            time.sleep(rd.randint(2,5))
            #raise

def sendEmailWithAttachments(receivers,subject,message,trials,attachment):
    #receivers: a list of strings, stores the email addresses of the receivers.
    #subject: a string, stores the subject of the email.
    #message: a string, stores the plain text of the email.
    #trials: one integer number. program will auto retry until the email is sent or the number of retrials exceeds this number.
    #attachment: a list of strings, stores the file paths that you want to attach in the email. e.g. ['~/hi.txt','./sendEmail.py']

    sender = 'shinsyzgz@sohu.com'

    body=MIMEMultipart()
    body['From'] =_format_addr( "Guangzhi ZHANG<%s>"%(sender))
    body['To'] = _format_addr("<%s>"%(','.join(receivers)))
    body['Subject'] = subject

    #msgString=('From: %s\n\nTo: %s\n\n\n'%(sender, ','.join(receivers)))
    msgString=''
    msgString=msgString+ '\n'+message
    message = MIMEText(msgString, 'plain', 'utf-8')

    body.attach(message)

    for f in attachment:
        att=MIMEApplication(open(f,'rb').read())
        att.add_header('Content-Disposition', 'attachment', filename=f)
        body.attach(att)

    host="smtp.sohu.com"
    user="shinsyzgz@sohu.com"
    pwd="881028zgz"
    sent=False
    count=0
    while not sent:
        count=count+1
        if count>trials:
            print 'ERROR: FAILED TO SEND EMAIL.'
            break
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(host,25)
            smtpObj.login(user,pwd)
            smtpObj.sendmail(sender, receivers, body.as_string())
            print "result sent to",receivers 
            sent=True
            smtpObj.close()
        except :
            print "sth. wrong when sending email. retrying no.", count
            sent=False
            smtpObj.close()
            time.sleep(rd.randint(2,5))
            #raise



if __name__=='__main__':
    rec=['zgz07ie@gmail.com','shinsy@foxmail.com']
    sub='test'
    sub2=u'测试附件'
    msg=u'你好, guangzhi'
    files=['readme.md','sendEmail.py']
    sendEmailWithAttachments(rec,sub2,msg,3,files)

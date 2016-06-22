import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from email import encoders
from email.mime.multipart import MIMEMultipart
import random as rd
import pdb
import time


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def sendEmail(receivers,subject,message,trials):
    sender = 'shinsyzgz@sohu.com'

    #msgString=('From: %s\n\nTo: %s\n\n\n'%(sender, ','.join(receivers)))
    msgString=''

    msgString=msgString+ '\n'+message


    message = MIMEText(msgString, 'plain', 'utf-8')
    message['From'] =_format_addr( "Guangzhi ZHANG<%s>"%(sender))
    message['To'] = _format_addr("<%s>"%(','.join(receivers)))

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
        except :
            print "sth. wrong when sending email. retrying no.", count
            sent=False
            time.sleep(rd.randint(2,5))
            raise

if __name__=='__main__':
    rec=['zgz07ie@gmail.com']
    sub='test'
    msg='hi, guangzhi'
    sendEmail(rec,sub,msg,3)

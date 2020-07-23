#coding=UTF8
"""
imap4 receive email
smtp send email
@author: 0yuchen.com, pything.com
"""
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import utils
from email.utils import COMMASPACE,formatdate
from email import encoders

import email 
import os
import smtplib 
import imaplib
import time

class Email:

    def __init__(self,smtp_server_name,imap_server_name,user,passwd):

        self.server = {}
        self.server["smtp_name"] = smtp_server_name
        self.server["imap_name"] = imap_server_name
        self.server["user"] = user
        self.server["passwd"] = passwd

        self.imap = imaplib.IMAP4_SSL(imap_server_name)
        self.imap.login(user,passwd)

        self.current_mailbox = ""


    def sendMail(self, fro, to, subject, text, files=[]): 
        """
        @param fro: from
        @type: str

        @param to: who receive
        @type: list

        @subject: unicode
        @text: unicode

        @param files: file path
        @type: list
        """
        assert type(to) == list 
        assert type(files) == list 
     
        msg = MIMEMultipart() 
        msg['From'] = fro 
        msg['Subject'] = subject.encode("u8")
        msg['To'] = COMMASPACE.join(to) #COMMASPACE==', ' 
        msg['Date'] = formatdate(localtime=True) 
        msg.attach(MIMEText(text.encode("u8"))) 
     
        for file in files: 
            part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data 
            part.set_payload(open(file, 'rb').read()) 
            encoders.encode_base64(part) 
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) 
            msg.attach(part) 
     
        smtp = smtplib.SMTP_SSL(self.server["smtp_name"],465)
        smtp.connect(self.server["smtp_name"])
        smtp.login(self.server['user'], self.server['passwd']) 
        smtp.sendmail(fro, to, msg.as_string()) 
        smtp.close()

    def getEnvelope(self,mailId):
        """
        获取信封，信封包含发件人，收件人，主题，发件时间
        """
        result = {}
        header = self.imap.fetch(mailId,"body[header]")[1][0][1]
#        print header
        header = email.message_from_string(header)
        result["from"] = header["from"]
        result["to"] = header["to"]
        result["time"] = self.internalDate2unixTime(header["date"])
        result["subject"] = header["subject"].decode("u8")
        return result

    def downloadAttachment(self,mailId, fileIndex,savePath):
        """
        下载附件
        @fileIndex: 附件的序号
        """
        content = self.imap.fetch(mailId, "body[%d]"%(fileIndex))[1][0][1]
        f = open(savePath, "wb")
        f.write(content.decode("base64"))
        f.close()

    def readMail(self, mailId):
        """
        @return: [content,attachment_structure]
        """

        bodyStructure = self.__getBodyStructure(mailId)
        if not isinstance(bodyStructure[0],tuple):
            bodyStructure = (bodyStructure,)
#        print bodyStructure
        charset = bodyStructure[0][2][1]
#        print charset
        encoding = bodyStructure[0][5]
#        print encoding
        content = self.imap.fetch(mailId,"body[1]")[1][0][1].decode(charset,"ignore")
        if encoding.lower() == "base64":
            content = content.decode("base64")
        attachmentStructure = self.getAttachmentStructure(bodyStructure)

        return content,attachmentStructure

    def __getBodyStructure(self,mailId):
        
        body = self.imap.fetch(mailId,"bodystructure")[1][0]
#        print body
        startStr = "BODYSTRUCTURE "
        startPos = body.find(startStr)
        body = body[startPos + len(startStr): -1]
    #    print body
        body = body.replace(" ",",").replace(")(","),(")
        NIL = None
        body = eval(body)
        return body

    def getAttachmentStructure(self,bodyStructure):
        """
        获取附件结构：文件名,字节大小,序号
        @return: [(name,size,encoding,index),...]
        """

        result = []
        body = bodyStructure
#        print body
    #    print len(body[0])
    #    print len(body)
        fileIndex = 0
        for i in body:
            fileIndex += 1
            if not i:
                continue
            if i[0] == "APPLICATION":
                fileName = i[2][-1] # 文件名
                fileCoding = i[2][-3] # 文件编码
                fileSize = i[-4] # 大小
                result.append((fileName, fileSize,fileIndex))
        return result

    def recvNewMail(self):
        """
        获取当前文件夹未读邮件, 如果没有选择过当前文件夹则当前文件夹为收件箱
        @return: [id,...] 
        """

        if not self.current_mailbox:
            self.imap.select()
        result,data = self.imap.search(None,"UNSEEN")
        data = data[0]
        if data:
            data = data.split()
            return data
        return []

    def getBoxList(self):
        """
        获取文件夹（邮箱）列表
        @rtype: list
        """
        return self.imap.list()[1]

    def getMailList(self,box_name="INBOX"):
        """
        获取指定文件夹内的邮件id, 同时将当前文件夹设置为box_name
        @return: [id,...]
        @rtype: list
        """
        self.current_mailbox = box_name
        num = self.imap.select(box_name)[1]
        num = int(num[0])
        if num:
            return list(range(1,num + 1))
        else:
            return []

    def __storeMail(self,mailIdList, cmd, flag):

        assert isinstance(mailIdList, list),u"maildList must be a list"

        for i in mailIdList:
            self.imap.store(i, cmd, flag)

    def delMail(self,mailIdList):
        """
        删除当前文件夹邮件
        @param mailIdList: 邮件id列表
        @type: list
        """

        self.__storeMail(mailIdList, "+FLAGS", "\\Deleted")

    def setMailSeen(self,mailIdList):
        """
        将当前文件夹邮件标为已读
        @param mailIdList: 邮件id列表
        @type: list
        """
        self.__storeMail(mailIdList, "+FLAGS", "\\Seen")
 
    def setMailUnSeen(self,mailIdList):
        """
        将当前文件夹邮件标为未读
        @param mailIdList: 邮件id列表
        @type: list
        """
        self.__storeMail(mailIdList, "-FLAGS", "\\Seen")
               

    def logout(self):

        self.imap.logout()

    def internalDate2unixTime(self,date):

        return time.mktime(utils.parsedate(date))

    def copy2mailBox(self,mailIdList,mailBoxName):

        assert isinstance(mailIdList, list),u"maildList must be a list"
        for i in mailIdList:
            self.imap.copy(i,mailBoxName)

if "__main__" == __name__:

    password = raw_input("password:")
    e = Email("smtp.qq.com","imap.qq.com","@qq.com",password)
#    e.sendMail("neverlike@vip.qq.com",["neverlike@vip.qq.com"],u"测试发送邮件",u"哈哈cadfds", [])
    print e.getBoxList()
#    print e.getMailList()
    print e.getMailList()
    print e.recvNewMail()
    mailId = raw_input("mail id:")
    print "from", e.getEnvelope(mailId)["from"]
    print "to",e.getEnvelope(mailId)["to"]
    print "time", e.getEnvelope(mailId)["time"]
    print "subject",e.getEnvelope(mailId)["subject"]
    #a = e.getAttachmentStructure(26)
    #print a
    print "content:", e.readMail(mailId)[0]
    e.setMailSeen([mailId])
    e.copy2mailBox([mailId],"Sent Messages")
    print "attachment:", e.readMail(mailId)[1]
    #e.downloadAttachment(26,2,"test.txt")

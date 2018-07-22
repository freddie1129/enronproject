import os
import datetime
from .Enronlib import EnronEmail
from enron.models import Email, ToEmail, CcEmail, BccEmail, Question
from enron.models import StaffName
from enron.models import StaffEmail
from pathlib import PurePath
from .emailconst import mailConstant
from enron.models import ToEmailNew

#mailpath = "/home/freddie/PycharmProjects/testdata/slinger-r"


mailpath = "/home/freddie/PycharmProjects/testdata/"

from multiprocessing import Pool as ThreadPool
from glob import glob


def run():
    pool = ThreadPool(10)
    mailpath = "/root/maildir/"

    subdir = glob(mailpath + '*/')
    result = pool.map(refreshToEmailTable, subdir)
    for e in result:
        print(e)
    print("finished************************")

def importData(mailpath):
    path1 = str(PurePath(mailpath).parent) + "/"
    dirPath = "Dir: " + mailpath
    print("START: " + str(datetime.datetime.now()) + " " + dirPath)
    email = EnronEmail()
    fileCount = 0
    for root, dirs, files in os.walk(mailpath):
        for name in files:
            filename = os.path.join(root, name)
            #path = str(PurePath(mailpath).parent)
            path =  filename.replace(path1, "")
            email.setValue(filename)
            if email.msgId == "null":
                continue
            #print(filename)
            mail = Email(emailId=email.msgId,
                             time=email.mailDate,
                             fromAddress=email.fromAddress,
                             subject=email.subject,
                             content=email.content,
                             path=path
                             )
            mail.save()
            fileCount += 1
            mailToList = [ToEmail(emailId=mail,
                                  fromAddress=email.fromAddress,
                                  receiverAddress=receiver_to) for index, receiver_to in enumerate(email.toAddress)]
            ToEmail.objects.bulk_create(mailToList)
            mailCcList = [CcEmail(emailId=mail,
                                  fromAddress=email.fromAddress,
                                  receiverAddress=receiver_cc) for index, receiver_cc in enumerate(email.ccAddress)]
            CcEmail.objects.bulk_create(mailCcList)

            mailbccList = [BccEmail(emailId=mail,
                                    fromAddress=email.fromAddress,
                                    receiverAddress=receiver_bcc) for index, receiver_bcc in enumerate(email.bccAddress)]
            BccEmail.objects.bulk_create(mailbccList)

            os.remove(filename)
    print("Totle: " + str(fileCount))
    print("END: " + str(datetime.datetime.now()) + " " + dirPath)
    return dirPath,fileCount


def refreshToEmailTable(mailpath):
    path1 = str(PurePath(mailpath).parent) + "/"
    dirPath = "Dir: " + mailpath
    print("START: " + str(datetime.datetime.now()) + " " + dirPath)
    email = EnronEmail()
    fileCount = 0


    staffEmailList = StaffEmail.objects.all()
    emailList = [staff.emailAddress for staff in staffEmailList]

    def getStaff(address):
        try:
            return staffEmailList[emailList.index(address)].staffName
        except:
            return None

    def getEmailType(senderName, receiverName):
        if senderName == None and receiverName == None:
            return mailConstant.email_type_unknow
        elif senderName != None and receiverName == None:
            return mailConstant.email_type_from
        elif senderName == None and receiverName != None:
            return mailConstant.email_type_to
        elif senderName != None and receiverName != None:
            return mailConstant.email_type_between
        else:
            return mailConstant.email_type_unset

    for root, dirs, files in os.walk(mailpath):
        for name in files:
            filename = os.path.join(root, name)
            path =  filename.replace(path1, "")
            email.setValue(filename)
            if email.msgId == "null":
                continue
            mail = Email(emailId=email.msgId,
                             time=email.mailDate,
                             fromAddress=email.fromAddress,
                             subject=email.subject,
                             content=email.content,
                             path=path
                             )
            mailToList = []
            for index, receiver_to in enumerate(email.toAddress):
                senderName = getStaff(email.fromAddress)
                receiverName = getStaff(receiver_to)
                toemail = ToEmailNew(
                                  emailId=mail,
                                  senderAddress=email.fromAddress,
                                  receiverAddress=receiver_to,
                                  senderName=senderName,
                                  receiverName=receiverName,
                                  emailType=getEmailType(senderName=senderName, receiverName=receiverName)
                                  )
                mailToList.append(toemail)
            ToEmailNew.objects.bulk_create(mailToList)
            os.remove(filename)
    print("Totle: " + str(fileCount))
    print("END: " + str(datetime.datetime.now()) + " " + dirPath)
    return dirPath,fileCount







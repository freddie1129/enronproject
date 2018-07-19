from enron.models import  Choice, Question, Email, Sender, ToEmail,CcEmail,BccEmail, ReceiverTo, ReceiverBCC,ReceiverCC
from enron.models import StaffName, StaffEmail
from multiprocessing import Process
from django.db import connection
import os
from .Enronlib import EnronEmail
mailpath = "/home/freddie/NLPProject/RawData/maildir/"
mailpath = "/home/freddie/NLPProject/maildir/"

def run():
    #getFileNumber()
    #checkoutName(mailpath)
    #p = Email.objects.raw('SELECT num as COUNT(email_id), name as sender FROM polls_email GROUP BY sender ORDER BY COUNT(email_id) DESC')
    #for item in p:
    #    print(item.num + " " + item.name)

    # p1 = Process(target=updateSender)
    # p1.start()
    # p1.join()
    #
    # p2 = Process(target=updateReceiverTo)
    # p2.start()
    # p2.join()
    #
    # p3 = Process(target=updateReceiverBcc)
    # p3.start()
    # p3.join()
    #
    # p4 = Process(target=updateReceiverCc)
    # p4.start()
    # p4.join()

    updateSender()
    updateReceiverTo()
    updateReceiverBcc()
    updateReceiverCc()



def getFileNumber():
    number = 0
    for root, dirs, files in os.walk(mailpath):
        for name in files:
            number += 1
            filename = os.path.join(root, name)
            print(filename)
    print("File Number: " + str(number))
    return number

def checkoutName(mailpath):
    dirs = os.listdir(mailpath)
    for client in dirs:
        first_name = client.split('-')[0];
        last_name = client.split('-')[1];

        reDirName =  client
        keyword = first_name+"@enron.com"

        emailList = Email.objects.filter(path__contains=reDirName);
        userEmailAddreddList = []
        print("looking for: " + keyword)
        for email in emailList:
            fromEmailList = Email.objects.filter(emailId=email.emailId).filter(fromAddress__contains=keyword)
            toEmailList = ToEmail.objects.filter(emailId=email.emailId).filter(receiverAddress__contains=keyword)
            ccEmailList = CcEmail.objects.filter(emailId=email.email_id).filter(receiverAddress__contains=keyword)
            bccEmailList = BccEmail.objects.filter(emailId=email.email_id).filter(receiverAddress__contains=keyword)

            senderAddress = [client.fromAddress for client in fromEmailList]
            toAddress = [client.receiverAddress for client in toEmailList]
            ccAddress = [client.receiverAddress for client in ccEmailList]
            bccAddress = [client.receiverAddress for client in bccEmailList]
            userEmailAddreddList = userEmailAddreddList + list(set(senderAddress + toAddress + ccAddress + bccAddress))
        print("emailList")
        userEmailAddreddList = list(set(userEmailAddreddList))
        print(userEmailAddreddList)
        staff = StaffName(name=client)
        staff.save()
        staffaddressList = [StaffEmail(staffname=staff,emailAddress=address) for address in userEmailAddreddList]
        StaffEmail.objects.bulk_create(staffaddressList)


        #for address in userEmailAddreddList:
        #    staffaddress = StaffEmail(staffname=staff.staffname,emailaddress=address)
        #    staffaddress




        # staff = StaffEmail(staffname=client)
        # staff.save()
        # reg = first_name + "@enron.com"
        # senders =  Sender.objects.filter(sender__contains=reg)
        # reTo = ReceiverTo.objects.filter(name__contains=reg)
        # reCc = ReceiverCC.objects.filter(name_contains=reg)
        # reBcc = ReceiverBCC.objects.filter(name_contains=reg)
        #
        # senderAddress = [client.sender for client in senders]
        # ToAddress = [client.name for client in reTo]
        # CcAddress = [client.name for client in reCc]
        # BccAddress = [client.name for client in reBcc]
        #
        # list(set(senderAddress + ToAddress + CcAddress + BccAddress));
        #
        #
        #
        #
        # inboxfile1 = mailpath + client + '/sent/1.'
        # print(inboxfile1)
        # if os.path.isfile(inboxfile1):
        #     email = EnronEmail()
        #     email.setValue(inboxfile1)
        #     if email.msgId == "invalid":
        #         print("break**************")
        #         break
        #     print(email.fromAddress)
        # else:
        #     print("File is not existed.")


        #Sender.objects.filter(sender__contains=first_name)



def updateSender():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(emailId), fromAddress FROM enron_email GROUP BY fromAddress ORDER BY COUNT(emailId) DESC")
        all = cursor.fetchall()
        print("sender start " + str(len(all)))
        for row in all:
            s = Sender(number=row[0],
                       sender=row[1]
                       )
            s.save()
        print("endsender")



def updateReceiverTo():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(emailId_id), receiverAddress FROM enron_toemail GROUP BY receiverAddress ORDER BY COUNT(emailId_id) DESC")
        all = cursor.fetchall()
        print("To start " + str(len(all)))
        for row in all:
            s = ReceiverTo(number=row[0],
                       name=row[1]
                       )
            s.save()
        print("endto")

def updateReceiverCc():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(emailId_id), receiverAddress FROM enron_ccemail GROUP BY receiverAddress ORDER BY COUNT(emailId_id) DESC")
        all = cursor.fetchall()
        print("cc start " + str(len(all)))
        for row in all:
            s = ReceiverCC(number=row[0],
                       name=row[1]
                       )
            s.save()
        print("endcc")


def updateReceiverBcc():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(emailId_id), receiverAddress FROM enron_bccemail GROUP BY receiverAddress ORDER BY COUNT(emailId_id) DESC")
        all = cursor.fetchall()
        print("bcc start " + str(len(all)))
        for row in all:
            s = ReceiverBCC(number=row[0],
                       name=row[1]
                       )
            s.save()
        print("endbcc")



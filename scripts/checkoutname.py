from enron.models import  Choice, Question, Email, Sender, ToEmail,CcEmail,BccEmail, ReceiverTo, ReceiverBCC,ReceiverCC
from enron.models import StaffName, StaffEmail
from multiprocessing import Process
from django.db import connection
import os
from .Enronlib import EnronEmail

from multiprocessing import Pool as ThreadPool
#from multiprocessing.dummy import Pool as ThreadPool
from glob import glob


mailpath = "/home/freddie/PycharmProjects/maildir/"
num = 0;

def run():
    pool = ThreadPool(50)

    # abpath = "/home/freddie/PycharmProjects/testdata/"
    mailpath = "/home/freddie/PycharmProjects/maildir/"

    dirs = os.listdir(mailpath)

    #subdir = glob(mailpath + '*/')
    for d in dirs:
        print(d)
    result = pool.map(checkoutv2, dirs)
    #for e in result:
    #    print(e)
    print("finished************************")


    checkout(mailpath)


def checkoutv2(client):

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
        ccEmailList = CcEmail.objects.filter(emailId=email.emailId).filter(receiverAddress__contains=keyword)
        bccEmailList = BccEmail.objects.filter(emailId=email.emailId).filter(receiverAddress__contains=keyword)

        senderAddress = [client.fromAddress for client in fromEmailList]
        toAddress = [client.receiverAddress for client in toEmailList]
        ccAddress = [client.receiverAddress for client in ccEmailList]
        bccAddress = [client.receiverAddress for client in bccEmailList]
        userEmailAddreddList = userEmailAddreddList + list(set(senderAddress + toAddress + ccAddress + bccAddress))
    print( keyword + "emailList")
    userEmailAddreddList = list(set(userEmailAddreddList))
    print(userEmailAddreddList)
    staff = StaffName(name=client)
    staff.save()
    staffaddressList = [StaffEmail(staffName=staff,emailAddress=address) for address in userEmailAddreddList]
    StaffEmail.objects.bulk_create(staffaddressList)


def checkout(mailpath):
    num = 0;
    dirs = os.listdir(mailpath)
    for client in dirs:
        first_name = client.split('-')[0];
        last_name = client.split('-')[1];

        reDirName =  client
        keyword = first_name+"@enron.com"

        emailList = Email.objects.filter(path__contains=reDirName);
        userEmailAddreddList = []
        num += 1
        print("looking for: " + str(num) + " " + keyword)
        for email in emailList:
            fromEmailList = Email.objects.filter(emailId=email.emailId).filter(fromAddress__contains=keyword)
            toEmailList = ToEmail.objects.filter(emailId=email.emailId).filter(receiverAddress__contains=keyword)
            ccEmailList = CcEmail.objects.filter(emailId=email.emailId).filter(receiverAddress__contains=keyword)
            bccEmailList = BccEmail.objects.filter(emailId=email.emailId).filter(receiverAddress__contains=keyword)

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
        staffaddressList = [StaffEmail(staffName=staff,emailAddress=address) for address in userEmailAddreddList]
        StaffEmail.objects.bulk_create(staffaddressList)
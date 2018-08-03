from enron.models import  Choice, Question, Email, Sender, ToEmail,CcEmail,BccEmail, ReceiverTo, ReceiverBCC,ReceiverCC
from enron.models import StaffName, StaffEmail,Alias,Aliasf
from enron.models import EmailWithAlias
from enron.models import EmailWithStaff
from enron.models import AnalysisResult
from enron.models import ToEmailNew,CcEmailNew,BccEmailNew
from enron.models import StaCommunication
from .emailconst import mailConstant
from django.db.models import Q
from django.db.models import Avg, Count

def run():
    alias()

def alias():
    staff_list =  StaffName.objects.all()[0:1]
    for index, staff in enumerate(staff_list):
        print("{0}:{1}**************************".format(index+1,staff.name))
        first_name = staff.name.split('-')[0]
        address_keyword = "@enron.com"
        staff_sender = ToEmailNew.objects.filter(Q(emailId__path__startswith=first_name) & Q(senderAddress__contains=first_name) & Q(senderAddress__contains=address_keyword))
        staff_receiver = ToEmailNew.objects.filter(Q(emailId__path__startswith=first_name) & Q(receiverAddress__contains=first_name) & Q(receiverAddress__contains=address_keyword))
        sender_alias = staff_sender.values('senderAddress').annotate(number = Count("senderAddress"))
        receiver_alias = staff_receiver.values('receiverAddress').annotate(number = Count("receiverAddress"))
        list_sender_email = [Aliasf(staff=staff,emailAddress = a["senderAddress"], type = "send", number = a["number"]) for a in sender_alias]
        list_receiver_email = [Aliasf(staff=staff,emailAddress = a["receiverAddress"], type = "send", number = a["number"]) for a in receiver_alias]
        Aliasf.objects.bulk_create(list_sender_email)
        Aliasf.objects.bulk_create(list_receiver_email)
        print("**************Send email alias******************")
        for p in list_sender_email:
            print("{0}:{1}".format(p.emailAddress,p.number))
        print("**************Receiver email alias********************")
        for p in list_receiver_email:
            print("{0}:{1}".format(p.emailAddress,p.number))
        alias = list(set([a["senderAddress"] for a in sender_alias] + [a["receiverAddress"] for a in receiver_alias]))
        list_alias = [Alias(staff=staff, emailAddress=a) for a in alias]
        Alias.objects.bulk_create(list_alias)
        print("\n")


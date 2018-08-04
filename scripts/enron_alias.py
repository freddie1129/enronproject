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
import re

def run():
    alias()

def alias():
    staff_list =  StaffName.objects.all()
    staff_list = [StaffName.objects.get(pk='mims-thurston-p'),

                  ]
    #StaffName.objects.get(pk='williams-w3'),
    #staff_list =  [StaffName.objects.get(pk='crandall-s'),
    #               StaffName.objects.get(pk='rodrigue-r'),
    #               StaffName.objects.get(pk='clair-c')]
    #

    for index, staff in enumerate(staff_list):
        print("{0}:{1}**************************".format(index+1,staff.name))
        first_name = staff.aliasName.split('-')[0]
        last_name = staff.aliasName.split('-')[-1]
        print(first_name)
        print(last_name)
        address_keyword = "@enron.com"
        pathkey=''

        pathkey = staff.name

        regex = ".*{0}+.*{1}+@enron.com".format(last_name, first_name)
        #staff_sender = ToEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(senderAddress__contains=first_name) & Q(senderAddress__contains=address_keyword))
        #staff_receiver = ToEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(receiverAddress__contains=first_name) & Q(receiverAddress__contains=address_keyword))
        #staff_receiver_cc = CcEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(receiverAddress__regex=first_name) & Q(receiverAddress__contains=address_keyword))
        #staff_receiver_bcc = BccEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(receiverAddress__contains=first_name) & Q(receiverAddress__contains=address_keyword))
        # staff_sender = ToEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(senderAddress__contains=first_name) & Q(senderAddress__contains=address_keyword))
        # staff_receiver = ToEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(receiverAddress__contains=first_name) & Q(receiverAddress__contains=address_keyword))

        staff_sender = ToEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(senderAddress__contains=first_name))
        staff_receiver = ToEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(receiverAddress__contains=first_name))
        staff_cc = CcEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(receiverAddress__contains=first_name))
        staff_bcc = BccEmailNew.objects.filter(Q(emailId__path__startswith=pathkey) & Q(receiverAddress__contains=first_name))


        sender_alias = staff_sender.values('senderAddress').annotate(number = Count("senderAddress"))
        receiver_alias = staff_receiver.values('receiverAddress').annotate(number = Count("receiverAddress"))
        cc_alias = staff_cc.values('receiverAddress').annotate(number = Count("receiverAddress"))
        bcc_alias = staff_bcc.values('receiverAddress').annotate(number = Count("receiverAddress"))

        list_sender_email = [Aliasf(staff=staff,emailAddress = a["senderAddress"], type = "sent", number = a["number"]) for a in sender_alias]
        list_receiver_email = [Aliasf(staff=staff,emailAddress = a["receiverAddress"], type = "to", number = a["number"]) for a in receiver_alias]
        list_cc_email = [Aliasf(staff=staff,emailAddress = a["receiverAddress"], type = "cc", number = a["number"]) for a in cc_alias]
        list_bcc_email = [Aliasf(staff=staff,emailAddress = a["receiverAddress"], type = "bcc", number = a["number"]) for a in bcc_alias]

        list_dipulicate = [];
        print("**************Send email alias******************")
        for item in list_sender_email:
            if re.search(regex,item.emailAddress) != None:
                print("{0}:{1}".format(item.emailAddress, item.number))
                list_dipulicate.append(item.emailAddress)
                item.save()
        print("**************Receiver email alias********************")
        for item in list_receiver_email:
            if re.search(regex,item.emailAddress) != None:
                list_dipulicate.append(item.emailAddress)
                print("{0}:{1}".format(item.emailAddress, item.number))
                item.save()
        print("**************cc email alias********************")
        for item in list_cc_email:
            if re.search(regex, item.emailAddress) != None:
                list_dipulicate.append(item.emailAddress)
                print("{0}:{1}".format(item.emailAddress, item.number))
                item.save()
        print("**************bcc email alias********************")
        for item in list_bcc_email:
            if re.search(regex, item.emailAddress) != None:
                list_dipulicate.append(item.emailAddress)
                print("{0}:{1}".format(item.emailAddress, item.number))
                item.save()



        alias = list(set(list_dipulicate))
        list_alias = [Alias(staff=staff, emailAddress=a) for a in alias]
        Alias.objects.bulk_create(list_alias)



        #Aliasf.objects.bulk_create(list_sender_email)
        #Aliasf.objects.bulk_create(list_receiver_email)
        #for p in list_sender_email:
        #    print("{0}:{1}".format(p.emailAddress,p.number))
        #for p in list_receiver_email:
        #    print("{0}:{1}".format(p.emailAddress,p.number))
        #alias = list(set([a["senderAddress"] for a in sender_alias] + [a["receiverAddress"] for a in receiver_alias]))
        #list_alias = [Alias(staff=staff, emailAddress=a) for a in alias]
        #Alias.objects.bulk_create(list_alias)
        #print("\n")
    #l = Aliasf.objects.values("emailAddress").annotate(number=Count("emailAddress"))
    #for item in l:
    #    item['emailAddress']

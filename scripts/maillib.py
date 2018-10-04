from enron.models import  Choice, Question, Email, Sender, ToEmail,CcEmail,BccEmail, ReceiverTo, ReceiverBCC,ReceiverCC
from enron.models import StaffName, StaffEmail
from enron.models import EmailWithAlias
from enron.models import EmailWithStaff
from enron.models import AnalysisResult
from enron.models import Alias
from enron.models import RawEmail,RawEmailFrom,RawEmailTo,RawEmailCc,RawEmailBCc
from enron.models import RawEmailFromCore,RawEmailToCore,RawEmailCcCore,RawEmailBCcCore
from enron.models import RawEmailToExternal, RawEmailBccExternal,RawEmailCcExternal,RawEmailFromExternal

from enron.models import ResultAddress,ResultAddressCore
from django.db.models import Q

from enron.models import RawCoreEmail

from enron.models import Aliasf

from enron.models import ToEmailNew,CcEmailNew,BccEmailNew
from enron.models import StaCommunication
from enron.models import StaffAnalysis
from enron.models import PersonAnalysis
from enron.models import Person


from enron.models import EmailBrief
from .emailconst import mailConstant

from enron.models import RawCoreEmail
import json
from multiprocessing import Process
from django.db import connection

from scripts.nlp_pre import preprocess
from scripts.topictest import topic
from scripts.topictest import topic_re,topic_re_V2

from scripts.nlp_pre import get_stemmed_content
from django.db.models import Avg, Count, Min, Sum, Max

import os
import math
from subprocess import *
import numpy as np

from .Enronlib import EnronEmail
mailpath = "/root/project/maildir/"

def run():
    #initPersonTable()
    #settingPersonTable()
    #topic_test()
    stress_calculation()


    #l = StaffAnalysis.objects.filter(name="allen-p")[0:1]
    #for idx, e in enumerate(l):

        #t = e.mails_to_core_total.split(",")
        #print("{0},{1},StaffAnalysis{2},{3},{4}".format(e.mails_to_core_total_len,
        #                                       e.mails_to_core_send_len,
        #                                       e.mails_to_core_receive_len,
        #                                       e.mails_to_ext_send_len,
        #                                       e.mails_to_ext_receive_len))

        #mails = RawEmailFrom.objects.filter(e_id__in=t).order_by("e_date")
        #for m in mails:
        #    print(m.e_date)
        #print(len(t),len(set(t)), mails.count())
        #for m in mails:
        #    print(m.e_from_name,m.e_to_name,m.e_id.e_id, m.e_date)

        #re = groupmail(mails)
        #topic_re(re)



    #for c in re[5:10]:
    #    print("++++{0} {1} ++++".format(c[0],c[1]))
    #    if len(c[2]) != 0:
    #        cal_topic_per_month(c[2])
    #    else:
    #        print("NoEmails in this Month")
    #
    #    print("")

#re = [[start,end,email_id_list,email_content_list].....]

def cal_topic_per_month(month_email_id_list):
    lines = []
    for month_ids in month_email_id_list:
        mails = RawEmailFrom.objects.filter(e_id__in = month_ids).order_by("e_date")
        monthcontent = str.join(" ", [get_stemmed_content(e.e_content) for e in mails])
        lines.append(monthcontent)
    topic(lines)


# calculate diversity, density, ratio, time_ratio
def cal_colum():
    l = StaffAnalysis.objects.all()
    for idx, e in enumerate(l):
        t = e.mails_to_core_total.split(",")
        t1 = e.mails_to_core_total_len

        s = e.mails_to_core_send.split(",")
        s1 = e.mails_to_core_send_len

        r = e.mails_to_core_receive.split(",")
        r1 = e.mails_to_core_receive_len


        es = e.mails_to_ext_send.split(",")
        es1 = e.mails_to_ext_send_len


        er = e.mails_to_ext_receive.split(",")
        er1 = e.mails_to_ext_receive_len

        p = len(list(set(s + r + es + er)))



        e.diversity = e.mails_to_core_contact_total_len

        if e.diversity != 0:
            e.density = p / e.diversity
        else:
            e.density = 0

        maxemailnumb = analysis_com_ratio(e.name)
        if maxemailnumb != 0:
            e.ratio = e.density / maxemailnumb  # communicatiion ratio
        else:
            e.ratio = 0

        mails = RawEmailFrom.objects.filter(e_id__in=t)
        dates = [e.e_date for e in mails]
        if len(dates) != 0:
            min_date = min(dates)
            max_date = max(dates)
            datebin = calDatebin(min_date,max_date)
            to_timestamp = np.vectorize(lambda x: x.timestamp())
            date_stamp = to_timestamp(dates)
            date_bin = to_timestamp(datebin)
            his = np.histogram(date_stamp,date_bin)
            e.time_ratio = np.std(his[0])           #communication time ratio
        e.save()
        print("Index: {0}, name: {1} diversity: {2}, density: {3}, ratio: {4}, time ratio: {5}".format(idx, e.name,
              e.diversity, e.density, e.ratio, e.time_ratio))


# groupmails by per date
def groupmail(mails):
    dates = [e.e_date for e in mails]
    if len(dates) != 0:
        min_date = min(dates)
        max_date = max(dates)
        date_bin = calDatebin(min_date,max_date)

        l = len(date_bin) - 1
        re = [[None, None,[]]] * l
        re = [[date_bin[idx],date_bin[idx + 1],[],[]] for idx,a in enumerate(re)]
        for m in mails:
            timestamp =  m.e_date
            for idx, e in enumerate(re):
                if timestamp >= e[0] and timestamp < e[1]:
                    re[idx][2].append(m.e_id)
                    re[idx][3].append(str.join(" ",get_stemmed_content(m.e_content)))
                    break
        return  re
    else:
        return False


def topic_test():
    persons = Person.objects.filter(topic_change=None)
    length = persons.count()
    for idx, p in enumerate(persons):
        print(length - idx, p.name)
        #print("{0},{1},{2},{3},{4},{5}".format(len(p.mails_to_core.split(",")),
        #                                   len(p.mails_to_core_send.split(",")),
        #                                   len(p.mails_to_core_receive.split(",")),
        #                                   len(p.mails_to_core_self.split(",")),
        #                                   len(p.mails_to_ext_send.split(",")),
        #                                   len(p.mails_to_ext_receive.split(","))))

        e_id_list = p.mails_to_core.split(",")
        mails = RawEmailFrom.objects.filter(e_id__in=e_id_list).order_by("e_date")
        ret = groupmail(mails)
        #for re in ret:
        #    print("{0},{1},{2},{3}".format(re[0],re[1],len(re[2]),len(re[3])))
        siminarity =  topic_re_V2(ret)
        p.topic_change = siminarity
        print(siminarity)
        p.save()

def stress_calculation():
    persons = Person.objects.filter(Q(relax_level=None) | Q(stress_level=None))
    length = persons.count()
    for idx, p in enumerate(persons):
        print(length - idx, p.name)
        e_id_list = p.mails_to_core_send.split(",") + p.mails_to_ext_send.split(",")
        mails = RawEmailFrom.objects.filter(e_id__in=e_id_list).order_by("e_date")
        ml = mails.count()
        print("Total: {0}".format(ml))
        relax = []
        stress = []
        for idx, m in enumerate(mails):
            content = str.join(" ", preprocess(m.e_content))
            ret = stressAnalysis(content)
            m.relax_level = ret[0]
            m.stress_level = ret[1]
            m.save()
            relax.append(m.relax_level)
            stress.append(m.stress_level)
            print("{0}: {1} - {2}".format(ml - idx, m.relax_level, m.stress_level))
        print(relax)
        print(stress)
        average_relax = np.mean(relax)
        average_stress = np.mean(stress)
        p.relax_level = average_relax
        p.stress_level = average_stress
        print(average_relax,average_stress)

        p.save()





def addMonth(source):
    old_year = source.year
    old_month = source.month

    if (old_month + 1) % 13 == 0:
        new_month = 1
        new_year = old_year + 1
    else:
        new_month = old_month + 1
        new_year = old_year
    return datetime.datetime(year=new_year,month=new_month,day=1)

def calDatebin(start,end):
    bin = [start,]
    cur = start
    while cur < addMonth(end):
        tmp = addMonth(cur)
        bin.append(tmp)
        cur = tmp
    return bin




# select core staff's email and import them into RawEmailSamll
def initCoreEmail():
    staffList = Alias.objects.filter(isTrust=True)
    staffNameList = [staff.emailAddress for staff in  staffList]
    emails = RawEmail.objects.filter(e_from__in = staffNameList)
    pass

def elibGetInvalidAddresses():
    staffList = Alias.objects.filter(isTrust=True)
    return [staff.emailAddress for staff in staffList]

def initRawEmailToTable():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM enron_rawemailfromcore")
        cursor.execute("DELETE FROM enron_rawemailtocore")
        cursor.execute("DELETE FROM enron_rawemailcccore")
        cursor.execute("DELETE FROM enron_rawemailbcccore")
        cursor.execute("INSERT INTO enron_rawemailfromcore select * FROM enron_rawemailfrom WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1)")
        cursor.execute("INSERT INTO enron_rawemailtocore select * FROM enron_rawemailto WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to IN(SELECT emailAddress FROM enron_alias where isTrust=1)")
        cursor.execute("INSERT INTO enron_rawemailcccore select * FROM enron_rawemailcc WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to IN(SELECT emailAddress FROM enron_alias where isTrust=1)")
        cursor.execute("INSERT INTO enron_rawemailbcccore select * FROM enron_rawemailbcc WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to IN(SELECT emailAddress FROM enron_alias where isTrust=1)")




#initialize ResultAddress Table
def initResultAddressTable():
    staffList = Alias.objects.filter(isTrust=True)
    staffNameList = [staff.emailAddress for staff in staffList]
    addressList = ResultAddress.objects.filter(address__in=staffNameList)
    i = 0
    print("Total: {0}".format(addressList.count()))
    for addressEntity in addressList:
        address = addressEntity.address
        addressEntity.sendNumber = RawEmailFrom.objects.filter(e_from=address).count()
        addressEntity.receiveToNumber = RawEmailTo.objects.filter(e_to=address).count()
        addressEntity.receiveCcNumber = RawEmailCc.objects.filter(e_to=address).count()
        addressEntity.receiveBccNumber = RawEmailBCc.objects.filter(e_to=address).count()
        addressEntity.save()
        i = i + 1
        print("{0}:{1},{2},{3},{4}".format(i,addressEntity.sendNumber,addressEntity.receiveToNumber,
                                           addressEntity.receiveCcNumber,addressEntity.receiveBccNumber))



#initialize ResultAddress Table
def initResultAddressCoreTable():
    staffList = Alias.objects.filter(isTrust=True)
    staffNameList = [staff.emailAddress for staff in staffList]
    for e in staffNameList:
        a = ResultAddressCore(address=e)
        a.save()

    staffList = Alias.objects.filter(isTrust=True)
    staffNameList = [staff.emailAddress for staff in staffList]
    addressList = ResultAddressCore.objects.filter(address__in=staffNameList)
    i = 0
    print("Total: {0}".format(addressList.count()))
    for addressEntity in addressList:
        address = addressEntity.address
        addressEntity.sendNumber = RawEmailFromCore.objects.filter(e_from=address).count()
        addressEntity.receiveToNumber = RawEmailToCore.objects.filter(e_to=address).count()
        addressEntity.receiveCcNumber = RawEmailCcCore.objects.filter(e_to=address).count()
        addressEntity.receiveBccNumber = RawEmailBCcCore.objects.filter(e_to=address).count()
        addressEntity.save()
        i = i + 1
        print("{0}:{1},{2},{3},{4}".format(i,addressEntity.sendNumber,addressEntity.receiveToNumber,
                                           addressEntity.receiveCcNumber,addressEntity.receiveBccNumber))


# get all emails sended by a given staff's
# remove emails which has same timestamp
# divide the emails into two parts, the first 3/4 as training subset and the latter 1/4 testing set
import csv
import datetime
def splitTimeLine(name):
    staff = StaffName.objects.get(pk = name)
    alias = Alias.objects.filter(staff=staff).filter(isTrust=True)
    addressList = [a.emailAddress for a in alias]
    starttime = datetime.datetime(year =1990, month=1, day=1)
    mails = RawEmailFromCore.objects.filter(e_from__in=addressList).filter(e_date__gt=starttime)

    #delete emails with the same timestamp
    value = set(map(lambda x: x.e_date, mails))
    newList = [[e for e in mails if e.e_date == x] for x in value]
    newMails = [e[0] for e in newList]

    newMails = sorted(newMails, key=lambda mail: mail.e_date)

    size = len(newMails)
    #first three quater 3/4
    firstPartIndex = int(size * 0.75)
    print("Total: {0}".format(size))
    print("First Part: {0}---{1}".format(0, firstPartIndex))
    print("Last Part: {0}----{1}".format(firstPartIndex + 1, size-1))
    #for e in newMails[0 : firstPartIndex]:
    #    print("{0},{1}".format(e.e_id, e.e_date))
    #print("=========================================")
    #for e in newMails[firstPartIndex + 1 :]:
    #    print("{0},{1},{2}".format(e.e_id, e.e_date, e.e_from))

    import os
    cwd = os.getcwd()
    print("Current path: {0}".format(cwd))
    with open("./enron/static/enron/a.csv",'w', newline='') as f:
        write = csv.writer(f)
        write.writerows([["dtg","value"]])
        write.writerows([[e.e_date,1] for e in newMails])

    return (newMails[0 : firstPartIndex], newMails[firstPartIndex + 1 : ])




def initResultAddressTable1():
    staffList = Alias.objects.filter(isTrust=True)
    staffNameList = [staff.emailAddress for staff in staffList]
    for e in staffNameList:
        a = ResultAddress(address=e)
        a.save()

def getFileNumber():
    number = 0
    for root, dirs, files in os.walk(mailpath):
        for name in files:
            number += 1
            filename = os.path.join(root, name)
            print(filename)
    print("File Number: " + str(number))
    return number

def initStaffNameTable():
    size = Email.objects.count()  
    emails = Email.objects.all()
    number = 0
    i = 0
    print("Emails: " + str(size) + "\n")
    while i < size:
        email = emails[i]
        i += 1
        s = StaffEmail.objects.filter(emailAddress=email.fromAddress)
        try:
            #print(email.staffName)
            #print(len(s))
            #print(s[0].staffName)
            #print(email.emailId)
            email.staffName = str(s[0].staffName)
            #print('name:' + email.staffName)
            email.save()
            number += 1
        except:  
            pass
    print("number:" + str(number))

def initAliasTable():
    size = Email.objects.count()
    emails = Email.objects.all()
    number = 0
    i = 0
    print('Email Number: {0}'.format(size))
    while i < size:
        email = emails[i]
        i += 1
        s = StaffEmail.objects.filter(emailAddredd=email.fromAddress)
        try:
            name = str(s[0].staffName)
            staff = StaffName.objects.get(pk=name)
            emailwithstaff = EmailWithStaff(emailId = email,staffName = staff)
            emailwithstaff.save()
        except:
            pass



def getEmailIndex(emaillist,address):
    try:
       return emaillist.index(address)
    except:
       return -1



def getEmailType(is_from, is_to):
    if is_from and is_to:
        return mailConstant.email_type_between
    elif is_from and not is_to:
        return mailConstant.email_type_from
    elif not is_from and is_to:
        return  mailConstant.email_type_to
    else:
        return mailConstant.email_type_unknow

def addStaffNameToEmail(emailTypeClass):
    size = emailTypeClass.objects.count()
    startpos = 260000
    emails = emailTypeClass.objects.all()[260000:]
    size = size - startpos
    number_from = 0
    number_to = 0
    number_between = 0
    i = 0
    class_name = emailTypeClass.__name__
    print('Add Staff Name To {0}'.format(class_name))
    print('Email Number: {0}'.format(size))
    staffList = StaffEmail.objects.all()
    emaillist = [staff.emailAddress for staff in staffList]
    nameList = [staff.staffName.name for staff in staffList]

    while i < size:
        email = emails[i]
        index = getEmailIndex(emaillist,email.fromAddress)
        if index != -1:
            nameFrom = nameList[index]
        else:
            nameFrom = mailConstant.string_unknown
        index = getEmailIndex(emaillist,email.receiverAddress)
        if index != -1:
            nameTo = nameList[index]
        else:
            nameTo = mailConstant.string_unknown
        email.staffNameFrom = nameFrom
        email.staffName = nameTo
        is_from = nameFrom != mailConstant.string_unknown
        is_to = nameTo != mailConstant.string_unknown
        email.emailType = getEmailType(is_from,is_to)
        email.save()
        if is_from and is_to:
            number_between += 1
            email.emailType = mailConstant.email_type_between
        if is_from:
            number_from += 1

        if is_to:
            number_to += 1
        if i % 1000 == 0:
            print('processed {0}\n'.format(i))
        email.save()
        i += 1

    if class_name == ToEmail.__name__:
        res = AnalysisResult(mailConstant.result_received_email_number_from_enron_group, '', number_from)
        res.save()
        print(res)
        res = AnalysisResult(mailConstant.result_received_email_number_from_external, '', size - number_from)
        res.save()
        print(res)
        res = AnalysisResult(mailConstant.result_received_email_number_to_enron_group, '', number_to)
        res.save()
        print(res)
        res = AnalysisResult(mailConstant.result_received_email_number_to_external, '', size - number_to)
        res.save()
        print(res)
        res = AnalysisResult(mailConstant.result_received_email_number_between_enron_group, '', number_between)
        res.save()
        print(res)


def addStaffNameToEmailV1(emailTypeClass):
    size = emailTypeClass.objects.count()
    emails = emailTypeClass.objects.all()
    number_from = 0
    number_to = 0
    number_between = 0
    i = 0
    class_name = emailTypeClass.__name__
    print('Add Staff Name To {0}'.format(class_name))
    print('Email Number: {0}'.format(size))
    staffNameList = StaffName.objects.all()

    while i < size:
        email = emails[i]
        s_from = StaffEmail.objects.filter(emailAddress=email.fromAddress)
        is_from = False
        is_to = False
        try:
            nameFrom = str(s_from[0].staffName)
            staff = StaffName.objects.get(pk=nameFrom)
            email.staffNameFrom = staff.name
            number_from += 1
            is_from = True
        except:
            email.staffNameFrom = ''
            is_from = False
            pass
        s_to = StaffEmail.objects.filter(emailAddress=email.receiverAddress)
        try:
            nameTo = str(s_to[0].staffName)
            staff = StaffName.objects.get(pk=nameTo)
            email.staffName = staff.name
            number_to += 1
            is_to = True
        except:
            email.staffName = ''
            is_to = False
            pass
        if i % 1000 == 0:
            print('processed {0}\n'.format(i))
        i += 1
        email.save()
        if is_from and is_to:
            number_between += 1

    if class_name == ToEmail.__name__:
        res = AnalysisResult(mailConstant.result_received_email_number_from_enron_group,'',number_from)
        res.save()
        print(res)
        res = AnalysisResult(mailConstant.result_received_email_number_from_external,'',size - number_from)
        res.save()
        print(res)
        res = AnalysisResult(mailConstant.result_received_email_number_to_enron_group,'',number_to)
        res.save()
        print(res)
        res = AnalysisResult(mailConstant.result_received_email_number_to_external,'', size - number_to)
        res.save()
        print(res)
        res = AnalysisResult(mailConstant.result_received_email_number_between_enron_group,'', number_between)
        res.save()
        print(res)


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

def analysis_mail():
    allStaff = StaffName.objects.all()
    for staff_a in allStaff:
        for staff_b in allStaff:
            to_mails = ToEmailNew.objects.filter(senderName_id=staff_a.name).filter(receiverName_id=staff_b.name)
            cc_mails = CcEmailNew.objects.filter(senderName_id=staff_a.name).filter(receiverName_id=staff_b.name)
            bcc_mails = BccEmailNew.objects.filter(senderName_id=staff_a.name).filter(receiverName_id=staff_b.name)
            toList = [str(mail) for mail in to_mails];
            ccList = [str(mail) for mail in cc_mails]
            bccList = [str(mail) for mail in bcc_mails]
            result = {"to": toList,
                      "cc": ccList,
                      "bcc" : bccList}
            s =  StaCommunication(staffName1=staff_a,
                                  staffName2=staff_b,
                                  toNumber=len(toList),
                                  ccNumber = len(ccList),
                                  bccNumber = len(bccList),
                                  record = json.dumps(result,sort_keys=False))
            s.save()


def analysis_cc_mail():
    pass

def analysis_bcc_mail():
    pass




def stressAnalysis(text):
    process = Popen(['java', '-jar', './scripts/TensiStrengthMain.jar', 'sentidata', './scripts/TensiStrength_Data/', 'explain', "text",
                     text, "urlencoded", "mood", "0"], stdout=PIPE, stderr=PIPE)
    line = process.stdout.readline().decode("utf-8")
    ret = line.split("+")
    if len(ret) >= 2:
        relax_level = int(ret[0])
        stress_level = int(ret[1])
        return (relax_level,stress_level)
    else:
        return (0,0)

def importStressData():
    logfile = open("importStressData.log", "w")
    allStaff = StaffName.objects.all()
    staffIndex = 0
    emailIndex = 0
    for staff in allStaff:
        staffIndex += 1
        staffList = Alias.objects.filter(staff=staff).filter(isTrust=True)
        addressList = [s.emailAddress for s in staffList]
        emailList = RawEmailFromCore.objects.filter(e_from__in=addressList)
        logline = "{0} staff name: {1}\n".format(staffIndex, staff.name)
        logfile.write(logline)
        print(logline)
        print("total: {0}".format(emailList.count()))
        for email in emailList:
            content = str.join(" ", preprocess(email.e_content))
            ret = stressAnalysis(content)
            if ret != False:
                email.relax_level = ret[0]
                email.stress_level = ret[1]
                email.save()
            else:
                errorLog = "    error:{0} {1}\n".format(email.e_id, email.e_path)
                print(errorLog)
                logfile.write(errorLog)
                email.relax_level = 0
                email.stress_level = 0
                email.save()
            if (emailIndex % 100 == 0):
                print("Finished: {0}".format(emailIndex))
            emailIndex += 1
    logfile.close()

def initStaffAnalysis2():
    #calculate total
    staffs = StaffAnalysis.objects.all()
    for idx,staff in enumerate(staffs):
        frommails = json.load(staff.mailsfrom)
        tomails = json.load(staff.mailsto)
        ccmails = json.load(staff.mailsto)
        bccmails = json.load(staff.mailsto)



def initPersonTable():
    staffs = StaffName.objects.all()
    for s in staffs:
        p = Person(name=s.name,type=mailConstant.analysis_type_training)
        p.save()
        p = Person(name=s.name,type=mailConstant.analysis_type_testing)
        p.save()

import  math

def settingPersonTable():

    def statistic(mails, condition, person):
        name = person.name

        person.mails_to_core_send = ""
        person.mails_to_core_receive = ""
        # Total Emails
        mails_group = mails.filter(condition).values("e_date","e_from","e_to").annotate(id=Max("e_id"))
        ids = [m["id"] for m in mails_group]
        mails_d = RawEmailFrom.objects.filter(e_id__in=ids).order_by("e_date")
        ids = [m.e_id for m in mails_d]
        person.mails_to_core = str.join(",",ids)
        print("Total emails: {0}".format(len(ids)))


        # time ratio


        dates = [e.e_date for e in mails_d]
        if len(dates) != 0:
            min_date = min(dates)
            max_date = max(dates)
            datebin = calDatebin(min_date, max_date)
            to_timestamp = np.vectorize(lambda x: x.timestamp())
            date_stamp = to_timestamp(dates)
            date_bin = to_timestamp(datebin)
            his = np.histogram(date_stamp, date_bin)
            time_ratio = np.std(his[0])  # communication time ratio
            print("ratio: {0}".format(person.time_ratio))






        # Core Sending Emails
        mails_group = mails.filter(condition, Q(e_from_name=name), ~Q(e_to_name=unknow)).values("e_date", "e_from", "e_to").annotate(id=Max("e_id"))
        ids = [m["id"] for m in mails_group]
        mails_d = RawEmailFrom.objects.filter(e_id__in=ids).order_by("e_date")
        ids = [m.e_id for m in mails_d]
        person.mails_to_core_send = str.join(",", ids)
        print("Sending emails core: {0}".format(len(ids)))

        # Core Receiving Emails
        mails_group = mails.filter(condition, ~Q(e_from_name=unknow), Q(e_to_name=name)).values("e_date", "e_from", "e_to").annotate(id=Max("e_id"))
        ids = [m["id"] for m in mails_group]
        mails_d = RawEmailFrom.objects.filter(e_id__in=ids).order_by("e_date")
        ids = [m.e_id for m in mails_d]
        person.mails_to_core_receive = str.join(",", ids)
        print("Receiving emails core: {0}".format(len(ids)))

        # External Sending Emails
        mails_group = mails.filter(condition, Q(e_from_name=name), Q(e_to_name=unknow)).values("e_date",
                                                                                                           "e_from",
                                                                                                           "e_to").annotate(
            id=Max("e_id"))
        ids = [m["id"] for m in mails_group]
        mails_d = RawEmailFrom.objects.filter(e_id__in=ids).order_by("e_date")
        ids = [m.e_id for m in mails_d]
        person.mails_to_ext_send = str.join(",", ids)
        print("Sending emails ext: {0}".format(len(ids)))

        # Sending Emails
        mails_group = mails.filter(condition, Q(e_from_name=unknow), Q(e_to_name=name)).values("e_date",
                                                                                                          "e_from",
                                                                                                          "e_to").annotate(
            id=Max("e_id"))
        ids = [m["id"] for m in mails_group]
        mails_d = RawEmailFrom.objects.filter(e_id__in=ids).order_by("e_date")
        ids = [m.e_id for m in mails_d]
        person.mails_to_ext_receive = str.join(",", ids)
        print("Receiving emails ext: {0}".format(len(ids)))

        # Self Emails
        mails_group = mails.filter(condition, Q(e_from_name=name),Q(e_to_name=name)).values("e_date", "e_from", "e_to").annotate(id=Max("e_id"))
        ids = [m["id"] for m in mails_group]
        mails_d = RawEmailFrom.objects.filter(e_id__in=ids).order_by("e_date")
        ids = [m.e_id for m in mails_d]
        person.mails_to_core_self = str.join(",", ids)
        print("self emails: {0}".format(len(ids)))

        # Contact Statistic
        mails_group = mails.filter(condition).values("e_date", "e_from", "e_to").annotate(id=Max("id"))
        ids = [m["id"] for m in mails_group]
        mails_d = RawEmailTo.objects.filter(id__in=ids).order_by("e_date")
        m_list_from =  mails_d.values("e_from_name").annotate(count=Count("e_from_name")).order_by()
        name_from = [m["e_from_name"] for m  in m_list_from]
        name_from_dic = {}
        for m in m_list_from:
            name_from_dic[m["e_from_name"]] = m["count"]

        person.staff_to_core_send = str.join(",", name_from)
        print("Sending name count {0}".format(len(name_from)))
        m_list_to =  mails_d.values("e_to_name").annotate(count=Count("e_to_name")).order_by()
        name_to = [m["e_to_name"] for m  in m_list_to]

        name_to_dic = {}
        for m in m_list_to:
            name_to_dic[m["e_to_name"]] = m["count"]


        person.staff_to_core_receive = str.join(",", name_to)
        print("Receiving name count {0}".format(len(name_to)))
        contact_total = list(set(name_to + name_from) - set([name,unknow]))
        person.staff_to_core = str.join(",", contact_total)
        print("Total contact {0}".format(len(contact_total)))

        name_dic = {}
        for name in contact_total:
            try:
                f = name_from_dic[name]
            except KeyError:
                f = 0
            try:
                t = name_to_dic[name]
            except KeyError:
                t = 0
            name_dic[name] = f + t

        #print(name_from_dic)
        #print(name_to_dic)
        #print(name_dic)

        dictList = []
        for key, value in name_dic.items():
            dictList.append([key, value])

        #print(dictList)

        max_com_count = 0
        if (len(dictList) >= 1):
            max_staff =  max(dictList, key=lambda item: item[1])
            max_com_count = max_staff[1]



        #print(max_staff[0],max_staff[1])

        person.diversity = len(contact_total)
        person.density = (len(person.mails_to_core_send.split(",")) + len(person.mails_to_core_receive.split(","))) / person.diversity
        if max_com_count != 0:
            person.ratio = person.density / max_com_count
        else:
            person.ratio = 0

        person.time_ratio = time_ratio
        print("=============================")
        print("diversity: {0} density: {1} ratio: {2} time_ratio: {3}".format(
            person.diversity,person.density,person.ratio,person.time_ratio
        ))
        print("=============================")


        person.save()



    unknow = "unknow"
    p_list = Person.objects.filter(type=mailConstant.analysis_type_training)
    idx = 0
    for p in p_list:
        idx += 1
        name = p.name
        p_test = Person.objects.get(name = name, type=mailConstant.analysis_type_testing)
        print("=== {0} {1} ===".format(idx,name))
        # Total including core send, core receive, external send, external receive
        mails = RawEmailTo.objects.filter(Q(e_date__gt="1990-01-01 00:00:00"), Q(e_to_name=name)|Q(e_from_name=name))
        mails_group = mails.values("e_date","e_from","e_to").annotate(id=Max("e_id"))
        ids = [m["id"] for m in mails_group]
        print("Total index {0}，{1}".format(len(set(ids)),len(ids)))
        mails_d = RawEmailFrom.objects.filter(e_id__in=ids).order_by("e_date")
        ids = [m.e_id for m in mails_d]
        print("Total {0} {1}".format(len(ids), len(set(ids))))
        k = math.floor(0.75 * len(ids))
        d = RawEmailFrom.objects.get(e_id=ids[k])
        dTime = d.e_date


        print("====================Training Set==================")
        condition =  Q(e_date__lte=dTime)
        statistic(mails, condition, p)
        p.time_divider = dTime
        p.divider_value = 0.75
        p.save()

        print("====================Testing Set===================")
        condition = Q(e_date__gt=dTime)
        statistic(mails, condition, p_test)
        p_test.time_divider = dTime
        p_test.divider_value = 0.75
        p_test.save()




def cal_PersonTable():
    l = Person.objects.all()
    for idx, e in enumerate(l):
        t = e.mails_to_core.split(",")

        s = e.mails_to_core_send.split(",")

        r = e.mails_to_core_receive.split(",")

        es = e.mails_to_ext_send.split(",")

        er = e.mails_to_ext_receive.split(",")

        p = len(list(set(s + r + es + er)))

        e.diversity = len(e.staff_to_core.split(","))

        if e.diversity != 0:
            e.density = p / e.diversity
        else:
            e.density = 0

        maxemailnumb = analysis_com_ratio(e.name)
        if maxemailnumb != 0:
            e.ratio = e.density / maxemailnumb  # communicatiion ratio
        else:
            e.ratio = 0

        mails = RawEmailFrom.objects.filter(e_id__in=t)
        dates = [e.e_date for e in mails]
        if len(dates) != 0:
            min_date = min(dates)
            max_date = max(dates)
            datebin = calDatebin(min_date, max_date)
            to_timestamp = np.vectorize(lambda x: x.timestamp())
            date_stamp = to_timestamp(dates)
            date_bin = to_timestamp(datebin)
            his = np.histogram(date_stamp, date_bin)
            e.time_ratio = np.std(his[0])  # communication time ratio
        e.save()
        print("Index: {0}, name: {1} diversity: {2}, density: {3}, ratio: {4}, time ratio: {5}".format(idx, e.name,
                                                                                                       e.diversity,
                                                                                                       e.density,
                                                                                                       e.ratio,
                                                                                                       e.time_ratio))


from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
def default(o):
    return o._asdict()
def initStaffAnalysis():
    staffList = StaffAnalysis.objects.all()[0:1]
    index = 0
    for staff in staffList:
        index += 1
        name = staff.name
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT e_id FROM `enron_rawemailfromcore` WHERE name = %s AND e_date > '1990-01-01 00:00:00' GROUP BY e_date,e_from",
        #                    (name,))
        #     rows = cursor.fetchall()
        #     to_id_list = [e[0] for e in rows]
        #     staff.mailsfrom = json.dumps(to_id_list)
        #     staff.mailsfromLen = len(to_id_list)




        ###################################
        with connection.cursor() as cursor:
            cursor.execute("SELECT e_id_id,e_date,e_from,e_to,e_from_name,e_to_name FROM enron_rawemailtocore WHERE e_from_name = %s OR e_to_name = %s AND e_date > '1990-01-01 00:00:00' GROUP BY e_date, e_from, e_to",
                           (name,name))
            rows = cursor.fetchall()
            id_list_core_to = [e[0] for e in rows]
            cursor.execute(
                "SELECT e_id_id FROM enron_RawEmailToExternal WHERE e_from_name = %s OR e_to_name = %s AND e_date > '1990-01-01 00:00:00' GROUP BY e_date, e_from, e_to",
                (name, name))
            rows = cursor.fetchall()



        mailto = RawEmailToCore.objects.filter(e_id__in=id_list).order_by("e_date")
        staff.mailsto = serialize('json', mailto, cls=DjangoJSONEncoder)
        staff.mailstoLen = len(mailto)
        list(set([mail.e_from_name for mail in mailto] + [mail.e_to_name for mail in mailto]) - set([name]))







        staff.save()

        #staff.mailsto = json.dumps(mail_list)
        #print(staff.mailsto)
        #print(mailto)

            #staff.mailsto = json.dumps(to_id_list)
            #staff.mailstoLen = len(to_id_list)
            #print(to_id_list)
            #print(len(to_id_list))

            #print(idList)
            #print("length: {0}".format(len(idList)))

        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT e_to_name FROM enron_rawemailtocore WHERE e_from_name = %s AND e_to_name <> %s GROUP BY e_to_name",
        #                    (name,name))
        #     rows = cursor.fetchall()
        #     to_staff_list_to = [e[0] for e in rows]
        #
        #     cursor.execute("SELECT e_from_name FROM enron_rawemailtocore WHERE e_from_name <> %s AND e_to_name = %s GROUP BY e_from_name",
        #                    (name,name))
        #     rows = cursor.fetchall()
        #     to_staff_list_from = [e[0] for e in rows]
        #     staff_list = list(set(to_staff_list_to + to_staff_list_from))
        #     staff.staff_to = json.dumps(staff_list)
        #     staff.staff_to_len = len(staff_list)
        #     print("staff: {0}{1}-{2}-{3}".format(name, len(to_staff_list_to),len(to_staff_list_from),len(staff_list)))
        #
        #
        #
        #     #print(to_staff_list)
        #     #print(len(to_staff_list))
        #
        # ##################################
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT e_id_id FROM `enron_rawemailcccore` WHERE e_from_name = %s OR e_to_name = %s = %s AND e_date > '1990-01-01 00:00:00' GROUP BY e_date,e_from,e_to",
        #                    (name,))
        #     rows = cursor.fetchall()
        #     to_id_list = [e[0] for e in rows]
        #     staff.mailscc = json.dumps(to_id_list)
        #     staff.mailsccLen = len(to_id_list)
        #
        #     #print(idList)
        #     #print("length: {0}".format(len(idList)))
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT name FROM `enron_rawemailcccore` WHERE name_from = %s AND name <> %s GROUP BY name",
        #                    (name,name))
        #     rows = cursor.fetchall()
        #     to_staff_list = [e[0] for e in rows]
        #     staff.staff_cc = json.dumps(to_staff_list)
        #     staff.staff_cc_len = len(to_staff_list)
        #
        # ##########################
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT e_id_id FROM `enron_rawemailbcccore` WHERE e_from_name = %s OR e_to_name = %s AND e_date > '1990-01-01 00:00:00' GROUP BY e_date,e_from,e_to",
        #                    (name,))
        #     rows = cursor.fetchall()
        #     to_id_list = [e[0] for e in rows]
        #     staff.mailsbcc = json.dumps(to_id_list)
        #     staff.mailsbccLen = len(to_id_list)
        #
        #     #print(idList)
        #     #print("length: {0}".format(len(idList)))
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT name FROM `enron_rawemailbcccore` WHERE name_from = %s AND name <> %s GROUP BY name",
        #                    (name,name))
        #     rows = cursor.fetchall()
        #     to_staff_list = [e[0] for e in rows]
        #     staff.staff_bcc = json.dumps(to_staff_list)
        #     staff.staff_bcc_len = len(to_staff_list)
        # print("{0} {1}: from num: {2}, to num: {3}, cc num: {4}, bcc num: {5}".format(index,name,staff.mailsfromLen,staff.mailstoLen,staff.mailsccLen,staff.mailsbccLen))
        # print("{0} {1}: from num staff: {2}, to num staff: {3}, cc num staff: {4}, bcc num staff: {5}".format(index,name,staff.staff_from_len,staff.staff_to_len,staff.staff_cc_len,staff.staff_bcc_len))
        # #staff.save()
    #allStaff = StaffName.objects.all()
    #aList = [StaffAnalysis(name=staff.name) for staff in allStaff]
    #StaffAnalysis.objects.bulk_create(aList)

# tag emails by sender's name
def tagAllRawEmails():
    emails = RawEmail.objects.all()
    num = emails.count()
    index = 0
    while index < num:
        e = emails[index]
        s = Alias.objects.filter(emailAddress=e.e_from)
        if s.count() >=1:
            # exist
            e.e_sender_name = s[0].staff.name
            e.save()
        index += 1
        if (index % 1000 == 0):
            print("Index：{0}".format(index))
    print("Done:{0}".format(index))

# tag emails set by name
def tagAllRawEmailsTo():
    emails = RawEmailTo.objects.all()
    num = emails.count()
    index = 0
    while index < num:
        e = emails[index]
        s = Alias.objects.filter(emailAddress=e.e_from)
        if s.count() >=1:
            e.e_form_name = s[0].staff.name
        s = Alias.objects.filter(emailAddress=e.e_to)
        if s.count() >= 1:
            e.e_to_name = s[0].staff.name
        e.save()
        index += 1
        if (index % 1000 == 0):
            print("Index：{0}".format(index))
    print("Done:{0}".format(index))

# tag emails by sender's name
def tagAllRawEmailsCc():
    emails = RawEmailCc.objects.all()
    num = emails.count()
    index = 0
    while index < num:
        e = emails[index]
        if s.count() >=1:
            e.e_form_name = s[0].staff.name
        s = Alias.objects.filter(emailAddress=e.e_to)
        if s.count() >= 1:
            e.e_to_name = s[0].staff.name
        e.save()
        index += 1
        if (index % 1000 == 0):
            print("Index：{0}".format(index))
    print("Done:{0}".format(index))

# tag emails by sender's name
def tagAllRawEmailsBcc():
    emails = RawEmailBCc.objects.all()
    num = emails.count()
    index = 0
    while index < num:
        e = emails[index]
        if s.count() >=1:
            e.e_form_name = s[0].staff.name
        s = Alias.objects.filter(emailAddress=e.e_to)
        if s.count() >= 1:
            e.e_to_name = s[0].staff.name
        e.save()
        index += 1
        if (index % 1000 == 0):
            print("Index：{0}".format(index))
    print("Done:{0}".format(index))









def analysis_sta_totals():
    # calculate communication diversity
    staff_list = StaffAnalysis.objects.all()
    for idx, staff in enumerate(staff_list):
        # the number of staffs this person contracted
        totalmails = list(set(json.loads(staff.mailsto) + json.loads(staff.mailscc) + json.loads(staff.mailsbcc)))
        for email_id in totalmails:
            email = RawEmailFromCore.objects.get(pk = email_id)
            EmailShot(email.e_id,email.e_date,email.e_from,email)
            pass
        staff.totalmails = json.dumps(totalmails)
        staff.totalmailsLen = len(totalmails)

        totalstaffs = list(set(json.loads(staff.staff_to) + json.loads(staff.staff_cc) + json.loads(staff.staff_bcc)))
        staff.total_staff = json.dumps(totalstaffs)
        staff.total_staff_len = len(totalstaffs)
        staff.save()
        print("{0}: {1},{2}".format(idx, staff.totalmailsLen,staff.total_staff_len))


def calculateStaffAnalysis():
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT COUNT(*) FROM ((SELECT COUNT(*) FROM enron_rawemailfromcore GROUP BY name) AS T)")
    #     row = cursor.fetchone()
    #     print(row[0])

    staffList = StaffAnalysis.objects.all()
    staffNameList = [a.name for a in staffList]
    for staff in staffList:
        print("Staff: {0}".format(staff.name))

        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM ((SELECT COUNT(*) FROM enron_rawemailtocore WHERE name_from = %s AND name <> %s GROUP BY name) as T)",
                           (staff.name, staff.name))
            row = cursor.fetchone()
            communicators_number = row[0]
            staff.diversity = communicators_number

        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(e_id_id) FROM enron_rawemailtocore WHERE (name_from=%s OR name=%s) AND e_date > %s GROUP BY e_date ORDER BY e_date DESC",
                           (staff.name, staff.name, "1990-01-01 00:00:00"))
            rows = cursor.fetchall()
            email_checked_id = [a[0] for a in rows]
            #print(email_checked_id)
            #print(len(email_checked_id))


        id_collection = "({0})".format(str.join(",", email_checked_id))
        print(id_collection)

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #emailexchange = RawEmailToCore.objects.filter(Q(name_from=staff.name) | Q(name=staff.name)).order_by("-e_date")
        emailexchange = RawEmailToCore.objects.filter(e_id__in=email_checked_id).order_by("-e_date")
        total = emailexchange.count()
        print("------total----------{0}-------------".format(total))
        if communicators_number != 0:
            density = total / communicators_number
        else:
            density = 0
        staff.density = density
        #communication ratio
        with connection.cursor() as cursor:
            #cursor.execute(
            #    "SELECT MAX(A) FROM ((SELECT COUNT(*) AS A FROM enron_rawemailtocore WHERE name_from = %s AND name <> %s GROUP BY name) as T)",
            #    (staff.name, staff.name))
            cursor.execute(
                "SELECT MAX(A) FROM ((SELECT COUNT(*) AS A FROM enron_rawemailtocore WHERE e_id_id IN %s GROUP BY name) as T)",
                (id_collection,))
            row = cursor.fetchone()
            maxcomm = row[0]
            if maxcomm != 0:
                staff.ratio = density / maxcomm
            else:
                staff.ratio = 0
            print("Max comm: {0}, density {1},ration {2}".format(maxcomm,density, staff.ratio))
        #time ration

        #for e in emailexchange:
        #    print("{0} {1}".format(e.e_date,e))


        print("Staff: {0}, communicator: {1}, Email Number: {2}, Density: {3} Ratio: {4}".format(staff.name, communicators_number,total,density,staff.ratio ))




    #
    #     #
    #     cursor.execute("SELECT COUNT(*) FROM enron_rawemailfromcore GROUP BY name")
    #     row = cursor.fetchall()
    #     print(len(row))


    # staffList = StaffAnalysis.objects.all()[0:10]
    # for staff in staffList:
    #     print("Staff: {0}".format(staff.name))
    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT COUNT(*) FROM enron_rawemailtocore WHERE name = %s AND name_from <> %s GROUP BY name", staff.name, staff.name)
    #         row = cursor.fetchone()
    #         print(row)




        # staff = StaffName.objects.get(pk=name)
        # staffAlias = Alias.objects.filter(staff=staff).filter(isTrust=True)
        # staffEmailAddress = [emailAddress for emailAddress in staffAlias]
        # toEmails = RawComm.objects.filter(staff_a=staff).exclude(staff_b=staff)
        #
        # toNumberQuery = toEmails.aggregate(Sum("number_a_b"))
        # toNumber = toNumberQuery['number_a_b__sum']
        #
        # receiveNumberQuery = toEmails.aggregate(Sum("number_b_a"))
        # receiveNumber = receiveNumberQuery['number_b_a__sum']
        #
        # otherStaffList = StaffName.objects.exclude(name=name)
        # toMailsFromThisStaff = []
        # for s in otherStaffList:
        #     item = toEmails.filter(staff_b=s)[0]
        #     if item.number_a_b != 0 and item.number_b_a != 0:
        #         data = json.loads(item.record)
        #         toMailsFromThisStaff.append((item, data))
        # toMailsFromThisStaff.sort(key=lambda x: x[0].number_a_b + x[0].number_b_a, reverse=True)
        #
        #
        #
        # pass

# step 1 initialize core email table
def initCoreDataset():
    with connection.cursor() as cursor:
        #cursor.execute("DELETE FROM enron_rawemailfromcore")
        cursor.execute("DELETE FROM enron_rawemailtocore")
        cursor.execute("DELETE FROM enron_rawemailcccore")
        cursor.execute("DELETE FROM enron_rawemailbcccore")

        #cursor.execute("INSERT INTO enron_rawemailfromcore(e_id, e_date, e_from, e_subject, e_content, e_path, e_from_name) SELECT email.e_id, email.e_date, email.e_from, email.e_subject, email.e_content, email.e_path,alias.staff_id FROM enron_rawemailfrom AS email INNER JOIN enron_alias AS alias ON email.e_from = alias.emailAddress AND isTrust=1")
        #cursor.execute("INSERT INTO enron_rawemailfromcore(e_id, e_date, e_from, e_subject, e_content, e_path, e_from_name) (SELECT email.e_id, email.e_date, email.e_from, email.e_subject, email.e_content, email.e_path, alias.staff_id FROM (SELECT * FROM enron_rawemailfrom WHERE e_from IN (SELECT emailAddress FROM enron_alias WHERE isTrust=1) LIMIT 1000) AS email INNER JOIN enron_alias AS alias ON email.e_from = alias.emailAddress LIMIT 100)")


        #cursor.execute("INSERT INTO enron_rawemailfromcore(e_id,e_date,e_from,e_subject,e_content,e_path) SELECT e_id,e_date,e_from,e_subject,e_content,e_path FROM enron_rawemailfrom WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1)")
        cursor.execute("INSERT INTO enron_rawemailtocore(e_id_id,e_date,e_from,e_to) SELECT e_id_id,e_date,e_from,e_to FROM enron_rawemailto WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1)")
        cursor.execute("INSERT INTO enron_rawemailcccore(e_id_id,e_date,e_from,e_to) SELECT e_id_id,e_date,e_from,e_to FROM enron_rawemailcc WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1)")
        cursor.execute("INSERT INTO enron_rawemailbcccore(e_id_id,e_date,e_from,e_to)  SELECT e_id_id,e_date,e_from,e_to FROM enron_rawemailbcc WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1)")


def initExternalDataset():
    with connection.cursor() as cursor:

        #cursor.execute("DELETE FROM enron_rawemailfromexternal")
        #cursor.execute(
        #    "INSERT INTO enron_rawemailfromexternal(e_id_id,e_date,e_from,e_to) SELECT e_id_id,e_date,e_from,e_to FROM enron_rawemailto WHERE e_from NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1)")


        cursor.execute("DELETE FROM enron_RawEmailToExternal")
        cursor.execute(
            "INSERT INTO enron_RawEmailToExternal(e_id_id,e_date,e_from,e_to) SELECT e_id_id,e_date,e_from,e_to FROM enron_rawemailto WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1)")

        cursor.execute("DELETE FROM enron_rawemailccexternal")
        cursor.execute(
            "INSERT INTO enron_rawemailccexternal(e_id_id,e_date,e_from,e_to) SELECT e_id_id,e_date,e_from,e_to FROM enron_rawemailcc WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1)")

        cursor.execute("DELETE FROM enron_rawemailbccexternal")
        cursor.execute(
            "INSERT INTO enron_rawemailbccexternal(e_id_id,e_date,e_from,e_to) SELECT e_id_id,e_date,e_from,e_to FROM enron_rawemailbcc WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1) AND e_to NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust=1)")




# step 2 insert staff name to the core tables
emaillist = RawEmailToExternal.objects.all()
def tagName(emaillist):
    index = 0
    print("Tag Bcc table. {0}".format(emaillist.count()))
    for email in emaillist:
        #al = Alias.objects.filter(emailAddress=email.e_to)
        #if al.count() >= 1:
        #    email.e_to_name = al[0].staff.name
        al = Alias.objects.filter(emailAddress=email.e_from)
        if al.count() >= 1:
            email.e_from_name = al[0].staff.name
        email.save()
        index += 1
        if index % 500 == 0:
            print("Bcc finish {0}".format(index))


def indexOf(list, e):
    try:
        return list.index(e)
    except ValueError:
        return False




def TagName_RawEmailTo():

    with connection.cursor() as cursor:
        cursor.execute("UPDATE enron_rawemailto SET e_from_name = 'unknow' WHERE e_from NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1)")
        cursor.execute("UPDATE enron_rawemailto SET e_to_name = 'unknow' WHERE e_to NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1)")

    staff_list = [s for s in StaffName.objects.all()]
    for idx, staff in enumerate(staff_list):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE enron_rawemailto SET e_from_name = %s WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1 AND staff_id = %s)",(staff.name,staff.name))
            cursor.execute("UPDATE enron_rawemailto SET e_to_name = %s WHERE e_to IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1 AND staff_id = %s)",(staff.name,staff.name))
        print("{0}:{1}".format(idx,staff.name))


def TagName_RawEmailCc():
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE enron_rawemailcc SET e_from_name = %s WHERE e_from NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1)",("unknow",))
        cursor.execute(
            "UPDATE enron_rawemailcc SET e_to_name = %s WHERE e_to NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1)",("unknow",))

    staff_list = [s for s in StaffName.objects.all()]
    for idx, staff in enumerate(staff_list):
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE enron_rawemailcc SET e_from_name = %s WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1 AND staff_id = %s)",
                (staff.name, staff.name))
            cursor.execute(
                "UPDATE enron_rawemailcc SET e_to_name = %s WHERE e_to IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1 AND staff_id = %s)",
                (staff.name, staff.name))
        print("tag cc {0}:{1}".format(idx, staff.name))

def TagName_RawEmailBcc():
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE enron_rawemailbcc SET e_from_name = %s WHERE e_from NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1)",("unknow",))
        cursor.execute(
            "UPDATE enron_rawemailbcc SET e_to_name = %s WHERE e_to NOT IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1)",("unknow",))

    staff_list = [s for s in StaffName.objects.all()]
    for idx, staff in enumerate(staff_list):
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE enron_rawemailbcc SET e_from_name = %s WHERE e_from IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1 AND staff_id = %s)",
                (staff.name, staff.name))
            cursor.execute(
                "UPDATE enron_rawemailbcc SET e_to_name = %s WHERE e_to IN(SELECT emailAddress FROM enron_alias WHERE isTrust = 1 AND staff_id = %s)",
                (staff.name, staff.name))
        print("tag bcc {0}:{1}".format(idx, staff.name))


def formail(list):
    return str.join(",",list)


def analysis_com_ratio(name):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT e_to_name, COUNT(*) as num FROM enron_rawemailto WHERE e_from_name = %s AND e_to_name <> %s AND e_to_name <> 'unknow' GROUP BY e_to_name",
            (name,name))
        to_summery = cursor.fetchall()
        #print(to_summery)

        cursor.execute(
            "SELECT e_from_name, COUNT(*) as num FROM enron_rawemailto WHERE e_to_name = %s AND e_from_name <> %s AND e_from_name <> 'unknow' GROUP BY e_from_name",
            (name, name))
        from_summery = cursor.fetchall()
        #print(from_summery)

        if len(to_summery) > len(from_summery):
            a_list = to_summery
            b_list = from_summery
        else:
            a_list = from_summery
            b_list = to_summery

        output = []
        for a in a_list:
            to_name = a[0]
            to_num = a[1]
            for b in b_list:
                if b[0] == to_name:
                    to_num += b[1]
                    break
            output.append((to_name,to_num))

        #print(output)
        if len(output) !=0 :
            m = max(output, key=lambda item: item[1])
            return m[1]
        else:
            return 0


def analysis_staff():
    staff_list = [s for s in StaffAnalysis.objects.all()[0:1]]
    start_time = "1990-01-01 00:00:00"
    staff_list = StaffAnalysis.objects.all()
    idx = 0
    for staff in staff_list:
        idx += 1

        with connection.cursor() as cursor:

            #operation in EailTo
            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailto WHERE (e_from_name = %s OR e_to_name = %s) AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, staff.name, start_time))
            rows = cursor.fetchall()
            id_toset_total = [a[0] for a in rows]

            cursor.execute("SELECT MAX(e_id_id) FROM enron_rawemailto WHERE (e_from_name = %s AND e_to_name <> 'unknow') AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",(staff.name,  start_time))
            rows = cursor.fetchall()
            id_toset_send_internal = [a[0] for a in rows]

            cursor.execute("SELECT MAX(e_id_id) FROM enron_rawemailto WHERE (e_from_name <> 'unkonw' AND e_to_name = %s) AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",( staff.name, start_time))
            rows = cursor.fetchall()
            id_toset_receive_internal = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailto WHERE (e_from_name = %s AND e_to_name = 'unknow') AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_toset_send_external = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailto WHERE (e_from_name = 'unknow' AND e_to_name = %s) AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_toset_receive_external = [a[0] for a in rows]
            print("To Email Subset: {0} {1}: {2},{3},{4},{5},{6}".format(idx, staff.name, len(id_toset_total),
                                                                         len(id_toset_send_internal),
                                                                         len(id_toset_receive_internal),
                                                                         len(id_toset_send_external),
                                                                         len(id_toset_receive_external)))

            staff.mails_to_core_total = str.join(",",id_toset_total)  #   json.dumps(id_toset_total)
            staff.mails_to_core_total_len = len(id_toset_total)
            staff.mails_to_core_send = str.join(",",id_toset_send_internal)  # json.dumps(id_toset_send_internal)
            staff.mails_to_core_send_len = len(id_toset_send_internal)
            staff.mails_to_core_receive = str.join(",",id_toset_receive_internal)  # json.dumps(id_toset_receive_internal)
            staff.mails_to_core_receive_len = len(id_toset_receive_internal)
            staff.mails_to_ext_send = str.join(",",id_toset_send_external)  # json.dumps(id_toset_send_external)
            staff.mails_to_ext_send_len = len(id_toset_send_external)
            staff.mails_to_ext_receive = str.join(",",id_toset_receive_external)  # json.dumps(id_toset_send_external)
            staff.mails_to_ext_receive_len = len(id_toset_receive_external)


            #operation in EailCC
            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailcc WHERE (e_from_name = %s OR e_to_name = %s) AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, staff.name, start_time))
            rows = cursor.fetchall()
            id_ccset_total = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailcc WHERE (e_from_name = %s AND e_to_name <> 'unknow') AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_ccset_send_internal = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailcc WHERE (e_from_name <> 'unknow' AND e_to_name = %s) AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_ccset_receive_internal = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailcc WHERE (e_from_name = %s AND e_to_name = 'unknow') AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_ccset_send_external = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailcc WHERE (e_from_name = 'unknow' AND e_to_name = %s) AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_ccset_receive_external = [a[0] for a in rows]
            print("CC Email Subset: {0} {1}: {2},{3},{4},{5},{6}".format(idx, staff.name, len(id_ccset_total),
                                                                         len(id_ccset_send_internal),
                                                                         len(id_ccset_receive_internal),
                                                                         len(id_ccset_send_external),
                                                                         len(id_ccset_receive_external)))
            staff.mails_cc_core_total = str.join(",", id_ccset_total)  # json.dumps(id_toset_total)
            staff.mails_cc_core_total_len = len(id_ccset_total)
            staff.mails_cc_core_send = str.join(",", id_ccset_send_internal)  # json.dumps(id_toset_send_internal)
            staff.mails_cc_core_send_len = len(id_ccset_send_internal)
            staff.mails_cc_core_receive = str.join(",",
                                                   id_ccset_receive_internal)  # json.dumps(id_toset_receive_internal)
            staff.mails_cc_core_receive_len = len(id_ccset_receive_internal)
            staff.mails_cc_ext_send = str.join(",", id_ccset_send_external)  # json.dumps(id_toset_send_external)
            staff.mails_cc_ext_send_len = len(id_ccset_send_external)
            staff.mails_cc_ext_receive = str.join(",", id_ccset_receive_external)  # json.dumps(id_toset_send_external)
            staff.mails_cc_ext_receive_len = len(id_ccset_receive_external)

            # operation in EailCC
            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailbcc WHERE (e_from_name = %s OR e_to_name = %s) AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, staff.name, start_time))
            rows = cursor.fetchall()
            id_toset_total = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailbcc WHERE (e_from_name = %s AND e_to_name <> 'unknow') AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_toset_send_internal = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailbcc WHERE (e_from_name <> 'unknow' AND e_to_name = %s) AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_toset_receive_internal = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailbcc WHERE (e_from_name = %s AND e_to_name = 'unknow') AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_toset_send_external = [a[0] for a in rows]

            cursor.execute(
                "SELECT MAX(e_id_id) FROM enron_rawemailbcc WHERE (e_from_name = 'unknow' AND e_to_name = %s) AND e_date > %s GROUP BY e_date,e_from,e_to ORDER BY e_date DESC",
                (staff.name, start_time))
            rows = cursor.fetchall()
            id_toset_receive_external = [a[0] for a in rows]
            print("BCC Email Subset: {0} {1}: {2},{3},{4},{5},{6}".format(idx, staff.name, len(id_toset_total),
                                                                         len(id_toset_send_internal),
                                                                         len(id_toset_receive_internal),
                                                                         len(id_toset_send_external),
                                                                         len(id_toset_receive_external)))

            staff.mails_bcc_core_total = str.join(",", id_toset_total)  # json.dumps(id_toset_total)
            staff.mails_bcc_core_total_len = len(id_toset_total)
            staff.mails_bcc_core_send = str.join(",", id_toset_send_internal)  # json.dumps(id_toset_send_internal)
            staff.mails_bcc_core_send_len = len(id_toset_send_internal)
            staff.mails_bcc_core_receive = str.join(",",
                                                   id_toset_receive_internal)  # json.dumps(id_toset_receive_internal)
            staff.mails_bcc_core_receive_len = len(id_toset_receive_internal)
            staff.mails_bcc_ext_send = str.join(",", id_toset_send_external)  # json.dumps(id_toset_send_external)
            staff.mails_bcc_ext_send_len = len(id_toset_send_external)
            staff.mails_bcc_ext_receive = str.join(",", id_toset_receive_external)  # json.dumps(id_toset_send_external)
            staff.mails_bcc_ext_receive_len = len(id_toset_receive_external)

            # analysis communicationor To Email
            cursor.execute(
                "SELECT e_to_name FROM enron_rawemailto WHERE e_from_name = %s AND e_to_name <> %s AND e_to_name <> 'unknow' GROUP BY e_to_name",
                (staff.name, staff.name))
            rows = cursor.fetchall()
            send_name = [a[0] for a in rows]

            cursor.execute(
                "SELECT e_from_name FROM enron_rawemailto WHERE e_from_name <> %s AND e_from_name <> 'unknow' AND e_to_name = %s GROUP BY e_from_name",
                (staff.name, staff.name))
            rows = cursor.fetchall()
            receive_name = [a[0] for a in rows]
            total_name = list(set(send_name + receive_name))
            print("To Email Subset Staff: {0} {1}: {2},{3},{4}".format(idx,
                                                                       staff.name,
                                                                       len(total_name),
                                                                       len(send_name),
                                                                       len(receive_name)
                                                                       ))

            staff.mails_to_core_contact_total = str.join(",",total_name)  #json.dumps(total_name)
            staff.mails_to_core_contact_total_len = len(total_name)
            staff.mails_to_core_contact_send = str.join(",",send_name) #json.dumps(send_name)
            staff.mails_to_core_contact_send_len = len(send_name)
            staff.mails_to_ext_contact_receive = str.join(",",receive_name) #json.dumps(receive_name)
            staff.mails_to_ext_contact_receive_len = len(receive_name)

            # analysis communicationor To Email
            cursor.execute(
                "SELECT e_to_name FROM enron_rawemailcc WHERE e_from_name = %s AND e_to_name <> %s AND e_to_name <> 'unknow' GROUP BY e_to_name",
                (staff.name, staff.name))
            rows = cursor.fetchall()
            send_name = [a[0] for a in rows]

            cursor.execute(
                "SELECT e_from_name FROM enron_rawemailcc WHERE e_from_name <> %s AND e_from_name <> 'unknow' AND e_to_name = %s GROUP BY e_from_name",
                (staff.name, staff.name))
            rows = cursor.fetchall()
            receive_name = [a[0] for a in rows]
            total_name = list(set(send_name + receive_name))
            print("Cc Email Subset Staff: {0} {1}: {2},{3},{4}".format(idx,
                                                                       staff.name,
                                                                       len(total_name),
                                                                       len(send_name),
                                                                       len(receive_name)
                                                                       ))

            staff.mails_cc_core_contact_total = str.join(",", total_name)  # json.dumps(total_name)
            staff.mails_cc_core_contact_total_len = len(total_name)
            staff.mails_cc_core_contact_send = str.join(",", send_name)  # json.dumps(send_name)
            staff.mails_cc_core_contact_send_len = len(send_name)
            staff.mails_cc_ext_contact_receive = str.join(",", receive_name)  # json.dumps(receive_name)
            staff.mails_cc_ext_contact_receive_len = len(receive_name)

            # analysis communicationor To Email
            cursor.execute(
                "SELECT e_to_name FROM enron_rawemailbcc WHERE e_from_name = %s AND e_to_name <> %s AND e_to_name <> 'unknow' GROUP BY e_to_name",
                (staff.name, staff.name))
            rows = cursor.fetchall()
            send_name = [a[0] for a in rows]

            cursor.execute(
                "SELECT e_from_name FROM enron_rawemailbcc WHERE e_from_name <> %s AND e_from_name <> 'unknow' AND e_to_name = %s GROUP BY e_from_name",
                (staff.name, staff.name))
            rows = cursor.fetchall()
            receive_name = [a[0] for a in rows]
            total_name = list(set(send_name + receive_name))
            print("Bcc Email Subset Staff: {0} {1}: {2},{3},{4}".format(idx,
                                                                       staff.name,
                                                                       len(total_name),
                                                                       len(send_name),
                                                                       len(receive_name)
                                                                       ))

            staff.mails_bcc_core_contact_total = str.join(",", total_name)  # json.dumps(total_name)
            staff.mails_bcc_core_contact_total_len = len(total_name)
            staff.mails_bcc_core_contact_send = str.join(",", send_name)  # json.dumps(send_name)
            staff.mails_bcc_core_contact_send_len = len(send_name)
            staff.mails_bcc_ext_contact_receive = str.join(",", receive_name)  # json.dumps(receive_name)
            staff.mails_bcc_ext_contact_receive_len = len(receive_name)

        staff.save()












def TagName_RawEmailToV2():
    emaillist = RawEmailTo.objects.all()[375500:]
    num = emaillist.count()
    index = 0
    print("Tag RawEmailTo Table. {0}".format(num))
    address = [e.emailAddress for e in Alias.objects.filter(isTrust=True)]
    name = [e.staff.name for e in Alias.objects.filter(isTrust=True)]
    while index < num:
        email = emaillist[index]
        from_index = indexOf(address,email.e_from)
        if from_index == False:
            email.e_from_name = "unknow"
        else:
            email.e_from_name = name[from_index]

        to_index = indexOf(address, email.e_to)
        if to_index == False:
            email.e_to_name = "unknow"
        else:
            email.e_to_name = name[to_index]
        email.save()
        index += 1
        if index % 500 == 0:
            print("Finished: {0}".format(index))





def setStaffNameForTables():
    emaillist = RawEmailFromCore.objects.all()
    print("Tag From table. {0}".format(emaillist.count()))
    index = 0
    for email in emaillist:
        al = Alias.objects.filter(emailAddress=email.e_from)
        if al.count() >= 1:
            email.e_from_name = al[0].staff.name
            email.save()
        index += 1
        if index % 500 == 0:
            print("From finish {0}".format(index))

    index = 0
    emaillist = RawEmailToCore.objects.all()
    print("Tag To table. {0}".format(emaillist.count()))
    for email in emaillist:
        al = Alias.objects.filter(emailAddress=email.e_to)
        if al.count() >= 1:
            email.e_to_name = al[0].staff.name
        al = Alias.objects.filter(emailAddress=email.e_from)
        if al.count() >= 1:
            email.e_from_name = al[0].staff.name
        email.save()
        index += 1
        if index % 500 == 0:
            print("To finish {0}".format(index))

    index = 0
    emaillist = RawEmailCcCore.objects.all()
    print("Tag Cc table. {0}".format(emaillist.count()))
    for email in emaillist:
        al = Alias.objects.filter(emailAddress=email.e_to)
        if al.count() >= 1:
            email.e_to_name = al[0].staff.name
        al = Alias.objects.filter(emailAddress=email.e_from)
        if al.count() >= 1:
            email.e_from_name = al[0].staff.name
        email.save()
        index += 1
        if index % 500 == 0:
            print("Cc finish {0}".format(index))

    print("Tag BCc table")
    index = 0
    emaillist = RawEmailBCcCore.objects.all()
    print("Tag Bcc table. {0}".format(emaillist.count()))
    for email in emaillist:
        al = Alias.objects.filter(emailAddress=email.e_to)
        if al.count() >= 1:
            email.e_to_name = al[0].staff.name
        al = Alias.objects.filter(emailAddress=email.e_from)
        if al.count() >= 1:
            email.e_from_name = al[0].staff.name
        email.save()
        index += 1
        if index % 500 == 0:
            print("Bcc finish {0}".format(index))

# step 3 calculate staff analysis data


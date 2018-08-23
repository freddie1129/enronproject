from django.shortcuts import render

from django.http import HttpResponse
from django.db.models import Sum
from django.db.models import Count

from enron.models import StaffName
from enron.models import Alias
from enron.models import Aliasf
from enron.models import RawComm

from enron.models import Email
from enron.models import StaffEmail
from django.db import connection

import os



from enron.models import StaCommunication

from scripts.test import history

import json

def index(request):
    staff_list = StaffName.objects.all()
    staff_data=[]
    for staff in staff_list:
        staff_list = StaCommunication.objects.filter(staffName1=staff)
        total_to = staff_list.aggregate(Sum('toNumber'))
        total_cc = staff_list.aggregate(Sum('ccNumber'))
        total_bcc = staff_list.aggregate(Sum('bccNumber'))
        staff_data.append( ( staff, total_to.get('toNumber__sum'), total_cc.get('ccNumber__sum'),total_bcc.get('bccNumber__sum')))
    context = {'staff_list': staff_data}
    return render(request, 'enron/index.html', context)

def home(request):
    return render(request, 'enron/index.html')



def staff_detail(request,staff_name):
    staff_list =  StaCommunication.objects.filter(staffName1=staff_name)
    total_to = staff_list.aggregate(Sum('toNumber'))
    total_cc = staff_list.aggregate(Sum('toNumber'))
    total_bcc = staff_list.aggregate(Sum('toNumber'))

    pass

def summery(request):
    staff_list = StaffName.objects.all()[0:100]
    brief = []
    for from_staff in staff_list:
        brief_row = [];
        for to_staff in staff_list:
            comm_between = StaCommunication.objects.filter(staffName1=from_staff).filter(staffName2=to_staff)[0]
            to_number = comm_between.toNumber
            cc_number = comm_between.ccNumber
            bcc_number = comm_between.bccNumber
            brief_row.append((from_staff.name,to_staff.name, to_number,cc_number,bcc_number))
        brief.append((from_staff.name,brief_row))
    contex = {'brief' : brief,
              'staff_list':[staff.name for staff in staff_list]}
    return render(request, 'enron/summery.html', contex)


# def email_matrix(request):
#     staff_list = StaffName.objects.all()[0:100]
#     brief = []
#     for from_staff in staff_list:
#         brief_row = []
#         for to_staff in staff_list:
#             comm_between = RawComm.objects.filter(staff_a=from_staff).filter(staff_b=to_staff)[0]
#             to_number = comm_between.toNumber
#             cc_number = comm_between.ccNumber
#             bcc_number = comm_between.bccNumber
#             brief_row.append((from_staff.name,to_staff.name, to_number,cc_number,bcc_number))
#         brief.append((from_staff.name,brief_row))
#     contex = {'brief' : brief,
#               'staff_list':[staff.name for staff in staff_list]}
#    return render(request, 'enron/summery.html', contex)


def email_matrix(request):
    staff_list = StaffName.objects.all()
    brief = []
    for from_staff in staff_list:
        brief_row = []
        for to_staff in staff_list:
            comm_between = RawComm.objects.filter(staff_a=from_staff).filter(staff_b=to_staff)[0]
            a_to_b = comm_between.number_a_b
            b_to_a = comm_between.number_b_a
            brief_row.append((from_staff.name,to_staff.name,a_to_b,b_to_a))
        brief.append((from_staff.name,brief_row))
    contex = {'brief' : brief,
              'staff_list':[staff.name for staff in staff_list]}
    return render(request, 'enron/summery.html', contex)





def email_timeline(request, staff_from, staff_to):
    contex = history(staff_from,staff_to)
    return render(request,'enron/a_b_history.html',contex)



def mail_history(request, staff_from, staff_to):
    detail_a_b = StaCommunication.objects.filter(staffName1=staff_from).filter(staffName2=staff_to)[0]
    detail_b_a = StaCommunication.objects.filter(staffName1=staff_to).filter(staffName2=staff_from)[0]

    mailList_a_b = json.loads(detail_a_b.record)
    mailList_b_a = json.loads(detail_b_a.record)

    a_to_b =  mailList_a_b['to']
    b_to_a =  mailList_b_a['to']

    a_b_list = [];
    for emaiId in a_to_b:
        e =  Email.objects.get(pk=emaiId)
        #a_b_list.append({"id":emaiId,"time": str(e.time)})
        a_b_list.append((True,emaiId,str(e.time)))

    b_a_list = [];
    for emaiId in b_to_a:
        e = Email.objects.get(pk=emaiId)
        # a_b_list.append({"id":emaiId,"time": str(e.time)})
        a_b_list.append((False,emaiId, str(e.time)))
    a_b_list = sorted(a_b_list, key=lambda email: email[2])


from enron.models import RawEmailFrom,RawEmailTo,RawEmailCc,RawEmailBCc
def mail_history_1(request, staff_from, staff_to):
    alias_a = Alias.objects.filter(staff=staff_from).filter(isTrust=True)
    address_a = [staff.emailAddress for staff in alias_a]
    alias_b = Alias.objects.filter(staff=staff_to).filter(isTrust=True)
    address_b = [staff.emailAddress for staff in alias_b]
    mail_a_b = RawEmailTo.objects.filter(x_from__in=address_a)


    mailList_a_b = json.loads(detail_a_b.record)
    mailList_b_a = json.loads(detail_b_a.record)

    a_to_b = mailList_a_b['to']
    b_to_a = mailList_b_a['to']

    a_b_list = [];
    for emaiId in a_to_b:
        e = Email.objects.get(pk=emaiId)
            # a_b_list.append({"id":emaiId,"time": str(e.time)})
        a_b_list.append((True, emaiId, str(e.time)))

        b_a_list = [];
    for emaiId in b_to_a:
        e = Email.objects.get(pk=emaiId)
            # a_b_list.append({"id":emaiId,"time": str(e.time)})
        a_b_list.append((False, emaiId, str(e.time)))
    a_b_list = sorted(a_b_list, key=lambda email: email[2])





    #json.dumps(a_b_list)

    #bcc_emails =  mailList['bcc']

    #contex = {"email" : json.dumps(a_b_list)}
    #contex = {"email" : json.dumps(a_b_list)}
    contex = {"a_email_b" : a_b_list}


    return render(request,'enron/a_email_b.html',contex)

# def staff_alias(request):
#     staff_list = StaffName.objects.all()
#     result = []
#     for idx, value in enumerate(staff_list):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM enron_staffemail WHERE id IN(SELECT MAX(id) FROM enron_staffemail WHERE staffName_id = %s GROUP BY emailAddress)", [value.name])
#             emails = cursor.fetchall()
#         if len(emails) == 0:
#             result.append((value.name, [('NA','untrusted')]))
#             continue
#         result.append((value.name, [(e[1], e[3]) for e in emails]))
#     contex = {"staff_list" : result}
#     return render(request, 'enron/staff-alias.html', contex)


def staff_alias(request):
    staff_list = StaffName.objects.all()
    result = []
    for idx, value in enumerate(staff_list):
        emails = StaffEmail.objects.filter(staffName=value)
        if len(emails) == 0:
            result.append((value.name, [('NA','untrusted')]))
            continue
        result.append((value.name, [(e.emailAddress, e.type) for e in emails]))
    contex = {"staff_list" : result}
    return render(request, 'enron/staff-alias.html', contex)

def staff_alias_a(request):
    staff_list = StaffName.objects.all()

    result = []
    for idx, staff in enumerate(staff_list):
        emails = Alias.objects.filter(staff=staff)
        if len(emails) == 0:
            result.append((staff.aliasName, [('NA',False)]))
            continue
        result.append((staff.aliasName, [(e.emailAddress, e.isTrust) for e in emails]))
    contex = {"staff_list" : result}
    return render(request, 'enron/staff-alias.html', contex)


def emailcontent(request, emailId):
    maildir = '/root/maildir/'
    email = Email.objects.get(pk=emailId)
    filepath =  maildir + email.path
    file = open(filepath, encoding="ISO-8859-1")
    text = file.read()
    file.close()
    contex = {"content": text,
              "path": filepath}
    return render(request, 'enron/rawcontent.html', contex)


def alais_process_log(request):
    return render(request, 'enron/staff-alias-process-log.html')


def staffsummery(request, staff_name):
    list =  StaCommunication.objects.filter(staffName1=StaffName.objects.get(pk=staff_name))
    list_to = list.exclude(toNumber=0)
    toNumber = list.aggregate(Sum('toNumber'))
    list_cc = list.exclude(ccNumber=0)
    ccNumber = list.aggregate(Sum('ccNumber'))
    list_bcc = list.exclude(bccNumber=0)
    bccNumber = list.aggregate(Sum('bccNumber'))
    contex = {"staff_name" : staff_name,
              "staff_to_num" : toNumber.get('toNumber__sum'),
              "staff_to_list": list_to,
              "staff_cc_num" : ccNumber.get('ccNumber__sum'),
              "staff_cc_list": list_cc,
              "staff_bcc_num" : bccNumber.get('bccNumber__sum'),
              "staff_bcc_list": list_bcc,}
    return render(request,'enron/staff_email_summery.html',contex)

def dirlist(request):
    list = StaffName.objects.all();
    contex ={ "staff_name_list" :  [staff.name for staff in list]}

    return render(request,'enron/dirlist.html',contex)


def my_custom_sql(name):
    #"arora-h%"
    with connection.cursor() as cursor:
        cursor.execute("select count(time), time, group_concat(emailId) from enron_email WHERE path like \'{0}%\' group by time order by count(time) desc".format(name))
        row = cursor.fetchall()
    return row

def sta_same_timestamp(request, dirname):
    emaillist =  Email.objects.filter(path__istartswith=dirname)
    #list = emaillist.values('time').annotate(dcount=Count('time')).order_by('-dcount')
    #list_content = emaillist.values('content').annotate(dcount=Count('content')).order_by('-dcount')
    id_list = my_custom_sql(name=dirname)

    #context = { 'list' : [(row.get('time'), row.get('dcount')) for row in list]}
    context = {'dir_name' : dirname,
        'list' : id_list}




    return render(request,'enron/sta_same_timestamp.html',context)
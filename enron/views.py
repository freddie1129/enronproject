from django.shortcuts import render

from django.http import HttpResponse
from django.db.models import Sum

from enron.models import StaffName
from enron.models import Email
from enron.models import StaffEmail



from enron.models import StaCommunication

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

def comm_brief(request):
    staff_list = StaffName.objects.all()[0:10]
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



    #json.dumps(a_b_list)

    #bcc_emails =  mailList['bcc']

    #contex = {"email" : json.dumps(a_b_list)}
    #contex = {"email" : json.dumps(a_b_list)}
    contex = {"a_email_b" : a_b_list}


    return render(request,'enron/a_email_b.html',contex)

def staff(request):
    result = [];
    staff_list = StaffName.objects.all()
    for idx, value in enumerate(staff_list):
        emails = StaffEmail.objects.filter(staffName=value)
        if len(emails) == 1:
            result.append((idx+1, value.name, len(emails), emails[0].emailAddress, []))
        else:
            result.append((idx+1, value.name, len(emails), emails[0].emailAddress, [e.emailAddress for e in emails[1:]]))
    contex = {"staff_list" : result}
    return render(request,'enron/staff.html',contex)

# Create your views here.

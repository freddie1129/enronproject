from django.shortcuts import render

from django.http import HttpResponse
from django.db.models import Sum

from enron.models import StaffName


from enron.models import StaCommunication

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

def staff_detail(request,staff_name):
    staff_list =  StaCommunication.objects.filter(staffName1=staff_name)
    total_to = staff_list.aggregate(Sum('toNumber'))
    total_cc = staff_list.aggregate(Sum('toNumber'))
    total_bcc = staff_list.aggregate(Sum('toNumber'))

    pass

def comm_brief(request):
    staff_list = StaffName.objects.all()
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

# Create your views here.

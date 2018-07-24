from django.shortcuts import render

from django.http import HttpResponse
from django.db.models import Sum

from enron.models import StaffName


from enron.models import StaCommunication

def index(request):
    staff_list = StaffName.objects.all()[0:2]
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


# Create your views here.

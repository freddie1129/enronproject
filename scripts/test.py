import sys
# Add the ptdraft folder path to the sys.path list
# sys.path.append('../')

from enron.models import StaffName, Alias, RawEmail,RawEmailFrom,RawEmailTo,RawEmailCc,RawEmailBCc
from django.db.models import Avg, Count
from enron.models import RawComm
from django.db.models import Q
import json

from itertools import groupby
from  operator import itemgetter

def run():
    #history('a','b')
    #ini_com()
    e = RawEmailTo.objects.filter(Q(e_date__gt="1990-01-01 00:00:00"), Q(e_from_name="allen-p") | Q(e_to_name="allen-p"))


def history(s_a, s_b):
    #s_a = 'allen-p'
    #s_b = 'dasovich-j'

    name_a = s_a
    staff_a = StaffName.objects.get(pk=name_a)
    add_list_a = Alias.objects.filter(staff=staff_a)
    email_address_list_a = [add.emailAddress for add in add_list_a]

    name_b = s_b
    staff_b = StaffName.objects.get(pk=name_b)
    add_list_b = Alias.objects.filter(staff=staff_b)
    email_address_list_b = [add.emailAddress for add in add_list_b]


    q_a_b = Q(e_from__in=email_address_list_a) & Q(e_to__in=email_address_list_b)
    q_b_a = Q(e_from__in=email_address_list_b) & Q(e_to__in=email_address_list_a)
    mails_a_b = RawEmailTo.objects.filter( q_a_b) #.order_by('e_date')
    mails_b_a = RawEmailTo.objects.filter( q_b_a) # .order_by('e_date')
    mails = [e for e in mails_a_b] + [e for e in mails_b_a]

    #for index, m in enumerate(mails):
    #    print("{0}:  {1}: {2} >>> {3}".format(index+1, m.e_date,m.e_from,m.e_to))

    value = set(map(lambda  x:x.e_date,mails))
    newList = [[e for e in mails if e.e_date == x]  for x in value]
    newMails = [e[0] for e in newList]
    newMails = sorted(newMails, key=lambda mail: mail.e_date)


    #print('***********************************************************')
    size_a = 0
    size_b = 0
    for index, m in enumerate(newMails):
        if m.e_from in email_address_list_a:
            size_a += 1
        elif m.e_from in email_address_list_b:
            size_b += 1
        #print("{0}:  {1}: {2} >>> {3}".format(index+1, m.e_date,m.e_from,m.e_to))

    contex = {'name_a':s_a,
              'name_b':s_b,
              'num_a_b': size_a,
              'num_b_a': size_b,
              'email_list': newMails}
    return contex


def ini_com():
    staff_list = StaffName.objects.all()
    for staff_a in staff_list:
        for staff_b in staff_list:
            context = history(staff_a.name, staff_b.name)
            email_list = [m.e_id.e_id for m in context.get('email_list')]
            s =  RawComm(staff_a = staff_a,
                         staff_b = staff_b,
                         number_a_b = context.get('num_a_b'),
                         number_b_a = context.get('num_b_a'),
                         record = json.dumps(email_list,sort_keys=False))
            s.save()

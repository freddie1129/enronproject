import re
import time
from enron.models import RawEmail,RawEmailTo,RawEmailCc,RawEmailBCc

def run():
    email_list = RawEmail.objects.all()
    for email in email_list:
        #str = "Tue, 28 Nov 2000 04:50:00 -0800 (PST)"
        #re_date = re.compile(r"(?P<date>\w\w\w, \d{1,2} \w\w\w \d\d\d\d \d\d:\d\d:\d\d [+-]\d\d\d\d).*")
        #m = re_date.match(email.e_date.strip())
        #str_date = m.group("date")
        #mail_date = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(str_date, "%a, %d %b %Y %H:%M:%S %z"))

        re_date = re.compile(r"(?P<date>\w\w\w, \d{1,2} \w\w\w \d\d\d\d \d\d:\d\d:\d\d [+-]\d\d\d\d).*")
        m = re_date.match(email.e_date.strip())
        str_date =  m.group("date")
        mail_date = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(str_date, "%a, %d %b %Y %H:%M:%S %z"))

        e_to_list = email.e_to.strip(",")
        email_to_list = [RawEmailTo(e_id=email,e_date = mail_date, e_from=email.e_from.strip(),e_to = to_addr) for to_addr in e_to_list]
        RawEmailTo.objects.bulk_create(email_to_list)

        e_cc_list = email.e_cc.strip(",")
        email_cc_list = [RawEmailTo(e_id=email,e_date = mail_date, e_from=email.e_from.strip(),e_to = to_addr) for to_addr in e_cc_list]
        RawEmailCc.objects.bulk_create(email_cc_list)

        e_bcc_list = email.e_bc.strip(",")
        email_bcc_list = [RawEmailTo(e_id=email,e_date = mail_date, e_from=email.e_from.strip(),e_to = to_addr) for to_addr in e_bcc_list]
        RawEmailBCc.objects.bulk_create(email_bcc_list)

import re
import time
from enron.models import RawEmail,RawEmailTo,RawEmailCc,RawEmailBCc
from django.core.exceptions import ValidationError

def run():
    email_list = RawEmail.objects.all()
    #email_number = Rawemail.objects.count();
    #print("Start: {0}\n".format(email_number))
    #print("Start: {0}\n".format(RawEmail.objects.count()))

    #for index, email in enumerate(email_list):
    index = 0
    while index < 517401:
        email = email_list[index]
        #str = "Tue, 28 Nov 2000 04:50:00 -0800 (PST)"
        try:
            strtime = email.e_date.strip()
            if strtime.find("0001") != -1:
                strtime = strtime.replace("0001","2001")
            elif strtime.find("0002") != -1:
                strtime = strtime.replace("0002", "2002")
            elif strtime.find("0003") != -1:
                strtime = strtime.replace("0003", "2003")
            elif strtime.find("0004") != -1:
                strtime = strtime.replace("0004", "2004")
            elif strtime.find("0005") != -1:
                strtime = strtime.replace("0005", "2005")
            elif strtime.find("0006") != -1:
                strtime = strtime.replace("0006", "2006")
            elif strtime.find("0007") != -1:
                strtime = strtime.replace("0007", "2007")
            elif strtime.find("0008") != -1:
                strtime = strtime.replace("0008", "2009")

            re_date = re.compile(r"(?P<date>\w\w\w, \d{1,2} \w\w\w \d\d\d\d \d\d:\d\d:\d\d [+-]\d\d\d\d).*")
            m = re_date.match(strtime)
            str_date =  m.group("date")
            mail_date = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(str_date, "%a, %d %b %Y %H:%M:%S %z"))

            e_to_list = email.e_to.split(",")
            email_to_list = [RawEmailTo(e_id=email,e_date = mail_date, e_from=email.e_from.strip(),e_to = to_addr.strip()) for to_addr in e_to_list]
            RawEmailTo.objects.bulk_create(email_to_list)

            e_cc_list = email.e_cc.split(",")
            email_cc_list = [RawEmailTo(e_id=email,e_date = mail_date, e_from=email.e_from.strip(),e_to = to_addr.strip()) for to_addr in e_cc_list]
            RawEmailCc.objects.bulk_create(email_cc_list)

            e_bcc_list = email.e_bcc.split(",")
            email_bcc_list = [RawEmailTo(e_id=email,e_date = mail_date, e_from=email.e_from.strip(),e_to = to_addr.strip()) for to_addr in e_bcc_list]
            RawEmailBCc.objects.bulk_create(email_bcc_list)

            if (index % 5000 == 0):
                print("Number: {0}\n".format(index))
        except ValidationError:
            print("Error: {0}\n", email.e_id)
        index += 1

    print("Processing End\n")
from enron.models import RawEmailFrom,RawEmailTo,RawEmailCc,RawEmailBCc
import os
import re
import time
from django.core.exceptions import ValidationError
oneMb = 1024 * 1024
mailpath = "/root/maildir/"
#mailpath = "/home/freddie/PycharmProjects/maildir"
def run():
    logpath = "import1.log"
    logfile = open(logpath,'w')
    for root, dirs, files in os.walk(mailpath):
        for name in files:
            filepath = os.path.join(root, name)
            print(filepath)
            fs = os.path.getsize(filepath)
            if fs > oneMb:
                print(filepath)
                logfile.write(filepath)
                logfile.write('\n')
                continue
            pro(filepath)
            os.remove(filepath)

def pro(filepath):
    file = open(filepath, encoding="ISO-8859-1")
    text = file.read()
    file.close()

    con = text.split("X-FileName:", 1)
    #email.e_content = con[1]
    text = con[0]
    text =  text.split("Message-ID:",1)
    text = text[1].split("\nDate:",1)
    e_id = text[0].strip()
    text =  text[1].split("\nFrom:",1)
    e_date = getDateTime(text[0].strip())
    e_to = None
    text = text[1].split("\nTo:",1)
    if (len(text) == 2):
        e_from = text[0].strip()
        text = text[1].split("\nSubject:", 1)
        e_to = text[0].strip()
        text = text[1].split("\nCc:", 1)
    else:
        text = text[0].split("\nSubject:", 1)
        e_from = text[0].strip()
        text = text[1].split("\nCc:", 1)

    e_cc = None
    if (len(text) == 2):
        e_subject = text[0].strip()
        text = text[1].split("\nMime-Version:", 1)
        e_cc = text[0].strip()
    else:
        text = text[0].split("\nMime-Version:", 1)
        e_subject = text[0].strip()
    #print(text)
    text = text[1].split("\nContent-Type:",1)
    #email.e_mime = text[0].strip()
    text = text[1].split("\nContent-Transfer-Encoding:",1)
    #email.e_type = text[0].strip()
    text = text[1].split("\nBcc:",1)
    e_bcc = None
    if (len(text) == 2):
        #email.e_encoding = text[0].strip()
        text = text[1].split("\nX-From:",1)
        e_bcc = text[0].strip()
    else:
        text = text[0].split("X-From:",1)
        #email.e_encoding = text[0].strip()
    text = text[1].split("X-To:",1)
    #email.e_x_from = text[0].strip()
    text = text[1].split("X-cc:",1)
    #email.e_x_to = text[0].strip()
    text = text[1].split("X-bcc:",1)
    #email.e_x_cc = text[0].strip()
    text = text[1].split("X-Folder:",1)
    #email.e_x_bcc = text[0].strip()
    text = text[1].split("X-Origin:",1)
    #email.e_x_folder = text[0].strip()
    text = text[1].split("X-FileName:",1)
    #email.e_x_origin = text[0].strip()
    text = con[1].split("\n",1)
    #email.e_x_filename = text[1].strip()
    e_content = text[1].strip()
    e_path = filepath.split(mailpath)[1]

    email = RawEmailFrom(e_id = e_id,
                         e_date = e_date,
                         e_from = e_from,
                         e_subject = e_subject,
                         e_path = e_path)
    try:
        email.save()
        if e_to != None:
            e_to_list = e_to.split(",")
            email_to_list = [RawEmailTo(e_id=email, e_date=e_date, e_from=e_from, e_to=to_addr.strip()) for
                             to_addr in e_to_list]
            RawEmailTo.objects.bulk_create(email_to_list)
        if e_cc != None:
            e_cc_list = e_cc.split(",")
            email_cc_list = [RawEmailTo(e_id=email, e_date=e_date, e_from=e_from, e_to=to_addr.strip()) for
                             to_addr in e_cc_list]
            RawEmailCc.objects.bulk_create(email_cc_list)
        if e_bcc != None:
            e_bcc_list = e_bcc.split(",")
            email_bcc_list = [RawEmailTo(e_id=email, e_date=e_date, e_from=e_from, e_to=to_addr.strip())
                          for to_addr in e_bcc_list]
            RawEmailBCc.objects.bulk_create(email_bcc_list)
    except ValidationError:
        print("Error: {0}\n", email.e_id)



def getDateTime(strtime):
    if strtime.find("0001") != -1:
        strtime = strtime.replace("0001", "2001")
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
    str_date = m.group("date")
    datetime =  time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(str_date, "%a, %d %b %Y %H:%M:%S %z"))
    return datetime
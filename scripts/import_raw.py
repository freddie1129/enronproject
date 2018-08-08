from enron.models import ToEmailNew,CcEmailNew,BccEmailNew,RawEmail
import os
oneMb = 1024 * 1024
mailpath = "/root/maildir/"
#mailpath = "/home/freddie/PycharmProjects/maildir"
def run():
    logpath = "import.log"
    logfile = open(logpath,'w')
    for root, dirs, files in os.walk(mailpath):
        for name in files:
            filepath = os.path.join(root, name)
            #print(filepath)
            fs = os.path.getsize(filepath)
            if fs > oneMb:
                print(filepath)
                logfile.write(filepath)
                logfile.write('\n')
                continue
            pro(filepath)


# def pro1(filepath):
#     file = open(filepath,encoding="ISO-8859-1")
#     text = file.read()
#     file.close()
#     email = RawEmail()
#     con = text.split("X-FileName:",1)
#     header = con[0]
#     content = con[1]
#     text = header.split("Message-ID:",1)
#     text = text[1].split("\nDate:",1)
#     email.e_id = text[0].strip()
#     text = text
#
#
#
#     content =  text.split("X-FileName:",1)[0]
#
#
#
#
#     text = text.find("Message-ID:",1                  )
#     text = text[1].split()

def pro(filepath):
    file = open(filepath, encoding="ISO-8859-1")
    text = file.read()
    file.close()
    email = RawEmail()

    con = text.split("X-FileName:", 1)
    #email.e_content = con[1]
    text = con[0]
    text =  text.split("Message-ID:",1)
    text = text[1].split("\nDate:",1)
    email.e_id = text[0].strip()
    text =  text[1].split("\nFrom:",1)
    email.e_date = text[0].strip()
    text = text[1].split("\nTo:",1)
    if (len(text) == 2):
        email.e_from = text[0].strip()
        text = text[1].split("\nSubject:", 1)
        email.e_to = text[0].strip()
        text = text[1].split("\nCc:", 1)
    else:
        text = text[0].split("\nSubject:", 1)
        email.e_from = text[0].strip()
        email.e_to=""
        text = text[1].split("\nCc:", 1)

    if (len(text) == 2):
        email.e_subject = text[0].strip()
        text = text[1].split("\nMime-Version:", 1)
        email.e_cc = text[0].strip()
    else:
        text = text[0].split("\nMime-Version:", 1)
        email.e_subject = text[0].strip()
        email.e_cc=""
    #print(text)
    text = text[1].split("\nContent-Type:",1)
    email.e_mime = text[0].strip()
    text = text[1].split("\nContent-Transfer-Encoding:",1)
    email.e_type = text[0].strip()
    text = text[1].split("\nBcc:",1)
    if (len(text) == 2):
        email.e_encoding = text[0].strip()
        text = text[1].split("\nX-From:",1)
        email.e_bcc = text[0].strip()
    else:
        text = text[0].split("X-From:",1)
        email.e_encoding = text[0].strip()
        email.e_bcc=""
    text = text[1].split("X-To:",1)
    email.e_x_from = text[0].strip()
    text = text[1].split("X-cc:",1)
    email.e_x_to = text[0].strip()
    text = text[1].split("X-bcc:",1)
    email.e_x_cc = text[0].strip()
    text = text[1].split("X-Folder:",1)
    email.e_x_bcc = text[0].strip()
    text = text[1].split("X-Origin:",1)
    email.e_x_folder = text[0].strip()
    text = text[1].split("X-FileName:",1)
    email.e_x_origin = text[0].strip()
    text = con[1].split("\n",1)
    email.e_x_filename = text[1].strip()
    email.e_content = text[1].strip()
    email.e_path = filepath.split(mailpath)[1]
    #print(email.e_path)
    email.save()
    #print(email.e_id)
    # print(email.e_date)
    # print(email.e_from)
    # print(email.e_to)
    # print(email.e_subject)
    # print(email.e_cc)
    # print(email.e_mime)
    # print(email.e_type)
    # print(email.e_encoding)
    # print(email.e_bcc)
    # print(email.e_x_from)
    # print(email.e_x_to)
    # print(email.e_x_bcc)
    # print(email.e_x_folder)
    # print(email.e_x_origin)
    # print(email.e_x_filename)
    # print(email.e_content)

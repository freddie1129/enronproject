import os
import re

import time
import mysql.connector
from mysql.connector import Error
from .Enronlib import EnronEmail
from polls.models import Choice, Question, EnEmail, EnEmailTo, EnEmailBcc, EnEmailCc


def addstaff2db(db, email_address, staff_name):
    dbcursor = db.cursor()
    if email_address == "arsystem@mailman.enron.com":
        print("Be careful")
    query = ("SELECT name FROM staffs WHERE email=\"%s\"" % (email_address))
    dbcursor.execute(query)
    staff_name_in_db = dbcursor.fetchall()
    if (len(staff_name_in_db) != 0):
        db_name = staff_name_in_db[0][0]
        if (db_name != staff_name):
            print("Error: %s" % (filename))
            print("Error: A staff seems using different name (db_email: %s, db_name: %s, latest_name: %s)" % (
            email_address, db_name, staff_name))
            ret = -1
        else:
            ret = 0;
    else:
        query_insert = "INSERT INTO staffs(email, name) VALUES(%s, %s)"
        dbcursor.execute(query_insert, (email_address, staff_name))
        ret = 1
    db.commit()
    dbcursor.close()
    return ret


def run():
    startTime = time.time()
    email = EnronEmail()
    fileCount = 0
    to_number = 0
    cc_number = 0
    bcc_number = 0

    mailpath = "/home/freddie/NLPProject/RawData/maildir_d"

    logfile = "./error_file_d.log"
    file_error = open(logfile, "w")
    for root, dirs, files in os.walk(mailpath):
        for name in files:
            global filename
            filename = os.path.join(root, name)
            path = filename.replace(mailpath, "")
            fileCount += 1
            email.setValue(filename)
            if email.msgId == "invalid":
                print("break**************")
                continue
            try:
                mail = EnEmail(email_id=email.msgId,
                             time=email.mailDate,
                             sender=email.fromAddress,
                             subject=email.subject,
                             content=email.content,
                             path=path
                             )
                mail.save()

                mailToList = [EnEmailTo(enemail=mail,
                                      sender=email.fromAddress,
                                      to_address=receiver_to) for receiver_to in enumerate(email.toAddress)]
                EnEmailTo.objects.bulk_create(mailToList)

                mailCcList = [EnEmailCc(enemail=mail,
                                      sender=email.fromAddress,
                                      cc_address=receiver_cc) for receiver_cc in enumerate(email.ccAddress)]
                EnEmailCc.objects.bulk_create(mailCcList)

                mailbccList = [EnEmailBcc(enemail=mail,
                                        sender=email.fromAddress,
                                        bcc_address=receiver_bcc) for receiver_bcc in enumerate(email.bccAddress)]
                EnEmailBcc.objects.bulk_create(mailbccList)
                os.remove(filename)
            except Error as error:
                print(error)
                print("error: " + error)
                file_error.write("error: " + error + " " + filename + "\n")

    strlog = "email Number:" + str(fileCount)
    print(strlog)
    file_error.write(strlog + "\n")
    strlog = "to Number:" + str(to_number)
    print(strlog)
    file_error.write(strlog + "\n")
    strlog = "cc Number:" + str(cc_number)
    print(strlog)
    file_error.write(strlog + "\n")
    strlog = "bcc Number:" + str(bcc_number)
    print(strlog)
    file_error.write(strlog + "\n")

    file_error.close()



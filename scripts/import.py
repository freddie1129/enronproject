import os
import re

import time
import mysql.connector
from mysql.connector import Error
from .Enronlib import EnronEmail
from polls.models import Choice, Question, Email, EmailTo, EmailBcc, EmailCc



def addstaff2db(db,email_address,staff_name):
    dbcursor = db.cursor()
    if email_address == "arsystem@mailman.enron.com":
        print("Be careful")
    query = ("SELECT name FROM staffs WHERE email=\"%s\""%(email_address))
    dbcursor.execute(query)
    staff_name_in_db = dbcursor.fetchall()
    if (len(staff_name_in_db) != 0):
        db_name = staff_name_in_db[0][0]
        if (db_name != staff_name):
            print("Error: %s"%(filename))
            print("Error: A staff seems using different name (db_email: %s, db_name: %s, latest_name: %s)"%(email_address, db_name, staff_name))
            ret = -1
        else:
            ret = 0;
    else:
        query_insert = "INSERT INTO staffs(email, name) VALUES(%s, %s)"
        dbcursor.execute(query_insert,(email_address,staff_name))
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

    mailpath="/home/freddie/NLPProject/testfile/allen-p"
    mailpath="/home/freddie/NLPProject/testfile/rapp-b"
    #mailpath="/home/freddie/NLPProject/maildir/kaminski-v/sent_items"
    mailpath = "/home/freddie/NLPProject/maildir"

    logfile = "./error_file.log"
    file_error = open(logfile, "w")
    for root, dirs, files in os.walk(mailpath):
        for name in files:
            global filename
            filename = os.path.join(root, name)
            path = filename.replace(mailpath, "")
            fileCount += 1
            #filelog = str(fileCount) + ":" + filename + "\n"
            #file_error.write(filelog)
            print(str(fileCount) + ":" + filename)
            email.setValue(filename)
            if email.msgId=="invalid":
                print("break**************")
                break
            try:
                mail = Email(email_id = email.msgId,
                            time = email.mailDate,
                            sender = email.fromAddress,
                            subject = email.subject,
                            content = email.content,
                            path = path
                            )
                mail.save()
                for idx, receiver_to in enumerate(email.toAddress):
                    mailTo = EmailTo(email_id = email.msgId,
                                        sender = email.fromAddress,
                                        to_address = receiver_to)
                    mailTo.save()
                    to_number += 1
                for idx,receiver_cc in enumerate(email.ccAddress):
                    mailCc = EmailCc(email_id=email.msgId,
                                        sender=email.fromAddress,
                                        cc_address=receiver_cc)
                    mailCc.save()
                    cc_number += 1
                for idx, receiver_bcc in enumerate(email.bccAddress):
                    mailBcc = EmailBcc(email_id=email.msgId,
                                        sender=email.fromAddress,
                                        bcc_address=receiver_bcc)
                    mailBcc.save()
                    bcc_number += 1
                os.remove(filename)
            except Error as error:
                print(error)
                print("error: " + error)
                file_error.write("error: " + error + " " + filename + "\n")

    file_error.close()
    strlog = "email Number:" + str(fileCount)
    print(strlog)
    file_error.write(str + "\n")
    strlog = "to Number:" + str(to_number)
    print(strlog)
    file_error.write(str + "\n")
    strlog = "cc Number:" + str(cc_number)
    print(strlog)
    file_error.write(str + "\n")
    strlog = "bcc Number:" + str(bcc_number)
    print(strlog)
    file_error.write(str + "\n")
    strlog = "elapsed time:", time.time() - startTime
    print(strlog)
    file_error.write(str + "\n")
    file_error.close()



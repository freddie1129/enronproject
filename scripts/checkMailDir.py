import os
import re
from enron.models import Email
from .Enronlib import EnronEmail
from django.core.exceptions import ObjectDoesNotExist

#mailpath = "/home/freddie/NLPProject/RawData"
mailpath = "/root/project/maildir/"




def run():
    logfile = "./lostFile.log"
    file = open(logfile, "w")
    number = 0;
    for root, dirs, files in os.walk(mailpath):
        for name in files:
            filename = os.path.join(root, name)
            with open(filename,encoding="ISO-8859-1") as f:
                s = f.readline()
                emailId = re.search(r"<(.+)>",s).group(1)
                try:
                    email = Email.objects.get(pk=emailId)
                except ObjectDoesNotExist:
                    email = None
                    number += 1
                    print("Lost " + str(number) + ": " + filename)
                    file.write(filename + "\n")
    file.close()
    



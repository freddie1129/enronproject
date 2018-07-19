import re
import time
import os

from pathlib import  PurePath

oneMb = 1024 * 1024


def logmail(mailPath, str):
    path = PurePath(mailPath)
    logfileName = "error.log"
    logfilePath = path.parent.joinpath(logfileName)

class EnronEmail:

    reEmail = re.compile(r"Message-ID: <(?P<messageid>.*)>\n"
                       r"Date: (?P<date>\w\w\w, \d{1,2} \w\w\w \d\d\d\d \d\d:\d\d:\d\d [+-]\d\d\d\d).*\n"
                       r"From: (?P<from>.*?)\n"
                       r"(To: )?(?P<to>.*)"
                       r"Subject: (?P<subject>.*)\n"
                       #r"(Cc: )?(?P<Cc>.*)"
                       r"Mime-Version: (?P<MimeVersion>.*)\n"
                       r"Content-Type: (?P<ContentType>.*)\n"
                       r"Content-Transfer-Encoding: (?P<Encoding>.*?)\n"
                       r"(Bcc: )?(?P<Bcc>.*)"
                       r"X-From: (?P<XFrom>.*)\n"
                       r"X-To: (?P<XTo>.*)\n"
                       r"X-cc: (?P<Xcc>.*)\n"
                       r"X-bcc: (?P<Xbcc>.*)\n"
                       r"X-Folder: (?P<XFolder>.*)\n"
                       r"X-Origin: (?P<XOrigin>.*)\n"
                       r"X-FileName: (?P<XFileName>.*?)\n"
                       r"(?P<Content>.*)", re.DOTALL)

    def __init__(self):
        self.msgId = ""
        self.mailDate = ""
        self.fromAddress = ""
        self.fromName = ""
        self.toAddress = []
        self.toNames = []
        self.ccAddress = []
        self.ccNames = []
        self.bccAddress = []
        self.bccNames = []
        self.subject = []
        self.content = []

    def cleanList(self,a):
        if (len(a) == 1 and a[0] == ""):
            a.clear()
        return



        with open(logfilePath, "a") as f:
            f.writelines(str)

    def setValue(self,filepath):
        text=''
        try:
            fs = os.path.getsize(filepath)
            if fs > oneMb:
                str = filepath + " ,Invalid: More Than 1MB"
                logmail(filepath, str)
                self.msgId = 'null'
                return
            file = open(filepath,encoding="ISO-8859-1")
            text = file.read()
            file.close()
        except ValueError:
            str = filepath + " ,Invalid: Read File"
            logmail(filepath, str )
            self.msgId='null'
            return

        m = self.reEmail.match(text)
        if m is not None:
            self.msgId = m.group("messageid")
            #print("dddddddd")
            #print(re.sub('[\t\n]', '', m.group("date")))
            datestring =  m.groups("date")
            #datestring.replace("0001","2001")
            strtime = re.sub('[\t\n]', '', m.group("date"))
            strtime_fix = strtime
            if strtime.find("0001") != -1:
                strtime_fix = strtime.replace("0001","2001")
            if strtime.find("0002") != -1:
                strtime_fix = strtime.replace("0002", "2002")
            if strtime.find("0003") != -1:
                strtime_fix = strtime.replace("0003", "2003")
            if strtime.find("0004") != -1:
                strtime_fix = strtime.replace("0004", "2004")
            if strtime.find("0005") != -1:
                strtime_fix = strtime.replace("0005", "2005")
            if strtime.find("0006") != -1:
                strtime_fix = strtime.replace("0006", "2006")
            if strtime.find("0007") != -1:
                strtime_fix = strtime.replace("0007", "2007")
            #print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
            #print(strtime_fix)
            #self.mailDate = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(m.group("date"), "%a, %d %b %Y %H:%M:%S %z"))
            self.mailDate = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(strtime_fix, "%a, %d %b %Y %H:%M:%S %z"))
            self.fromAddress = re.sub('[ \t\n]', '', m.group("from"))
            self.fromName = re.sub('[\t\n]', '', m.group("XFrom"))
            self.toAddress = re.sub('[ \t\n]', '', m.group("to")).split(",")
            self.toNames = re.sub('[\t\n]', '', m.group("XTo")).split(",")
            str = m.group("subject")
            if "\nCc: " in str:
                recc = re.compile("(?P<subject>.*)\n(Cc: )(?P<Cc>.*)", re.DOTALL)
                m1 = recc.match(str)
                self.subject = m1.group("subject")
                self.ccAddress = re.sub('[ \t\n]', '', m1.group("Cc")).split(",")
            else:
                self.subject = m.group("subject")
                self.ccAddress=[""]
            #self.ccAddress = re.sub('[\t\n]', '', m.group("Cc")).split(",")
            self.ccNames = re.sub('[\t\n]', '', m.group("Xcc")).split(",")
            self.bccAddress = re.sub('[ \t\n]', '', m.group("Bcc")).split(",")
            self.bccNames = re.sub('[\t\n]', '', m.group("Xbcc")).split(",")
            #self.subject = m.group("subject");
            self.content = m.group("Content");
            self.cleanList(self.toAddress)
            self.cleanList(self.toNames)
            self.cleanList(self.ccAddress)
            self.cleanList(self.ccNames)
            self.cleanList(self.bccAddress)
            self.cleanList(self.bccNames)
            #if (len(self.bccAddress) > 0):
            #    print("dd")
        else:
            print("Error: " + filepath)
        file.close()




from enron.models import ToEmailNew,CcEmailNew,BccEmailNew,RawEmail

def run():
    error_email = ToEmailNew.objects.filter(receiverAddress__contains="Subject")
    file = open("address_error_file.txt",'w')
    for idx, mail in enumerate(error_email):
        str = mail.receiverAddress
        file.write("{0}\n".format (mail.emailId))
        print("{0} Old Email Address {1}".format(idx,str))
        str = str.split("Subject")[0]
        mail.receiverAddress = str
        print("{0} Old Email Address {1}".format(idx,str))
        mail.save()
    file.close()



def pro():
    filepath = "testmail"
    file = open(filepath, encoding="ISO-8859-1")
    text = file.read()
    file.close()
    email = RawEmail()
    text =  text.split("Message-ID:")
    text = text[1].split("Date:")
    email.e_id = text[0]
    text =  text[1].split("From:")
    email.e_date = text[0]
    text = text[1].split("To:")
    email.e_from = text[0]
    text = text[1].split("Subject:")
    email.e_to = text[0]
    text = text[1].split("Cc:")
    email.e_subject = text[0]
    text = text[1].split("Mime-Version:")
    email.e_cc = text[0]
    text = text[1].split("Content-Type")
    email.e_mime = text[0]
    text = text[1].split("Content-Transfer-Encoding:")
    email.e_type = text[0]
    text = text[1].split("Bcc:")
    email.e_encoding = text[0]
    text = text[1].split("X-From:")
    email.e_bcc = text[0]
    text = text[1].split("X-To:")
    email.e_x_from = text[0]
    text = text[1].split("X-cc:")
    email.e_x_to = text[0]
    text = text[1].split("X-bcc:")
    email.e_x_cc = text[0]
    text = text[1].split("X-Folder:")
    email.e_x_bcc = text[0]
    text = text[1].split("X-Origin:")
    email.e_x_folder = text[0]
    text = text[1].split("X-FileName:")
    email.e_x_origin = text[0]
    text = text[1].split("\n")
    email.e_x_filename = text[0]
    email.e_content = text[1]




    # reEmail = re.compile(r"Message-ID: <(?P<messageid>.*)>\n"
    #                    r"Date: (?P<date>\w\w\w, \d{1,2} \w\w\w \d\d\d\d \d\d:\d\d:\d\d [+-]\d\d\d\d).*\n"
    #                    r"From: (?P<from>.*?)\n"
    #                    r"(To: )?(?P<to>.*)"
    #                    r"Subject: (?P<subject>.*)\n"
    #                    #r"(Cc: )?(?P<Cc>.*)"
    #                    r"Mime-Version: (?P<MimeVersion>.*)\n"
    #                    r"Content-Type: (?P<ContentType>.*)\n"
    #                    r"Content-Transfer-Encoding: (?P<Encoding>.*?)\n"
    #                    r"(Bcc: )?(?P<Bcc>.*)"
    #                    r"X-From: (?P<XFrom>.*)\n"
    #                    r"X-To: (?P<XTo>.*)\n"
    #                    r"X-cc: (?P<Xcc>.*)\n"
    #                    r"X-bcc: (?P<Xbcc>.*)\n"
    #                    r"X-Folder: (?P<XFolder>.*)\n"
    #                    r"X-Origin: (?P<XOrigin>.*)\n"
    #                    r"X-FileName: (?P<XFileName>.*?)\n"
    #                    r"(?P<Content>.*)", re.DOTALL)

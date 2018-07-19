from polls.models import Choice, Question, Email, EmailTo, EmailBcc, EmailCc

def run():
    deletedupicateEmailCc()
    deletedupicateEmailBcc()
    #deletedupicateEmailTo()

def deletedupicateEmail():
    emailTo = Email.objects.all()
    for emailTo in emailTo:
        list = Email.objects.filter(email_id=emailTo.email_id)
        justKeepFirstItem(list)

def deletedupicateEmailTo():
    emailTo = EmailTo.objects.all()
    for emailTo in emailTo:
        list = EmailTo.objects.filter(email_id=emailTo.email_id)
        justKeepFirstItem(list)

def deletedupicateEmailCc():
    emailTo = EmailCc.objects.all()
    for emailTo in emailTo:
        list = EmailCc.objects.filter(email_id=emailTo.email_id)
        justKeepFirstItem(list)

def deletedupicateEmailBcc():
    emailTo = EmailBcc.objects.all()
    for emailTo in emailTo:
        list = EmailBcc.objects.filter(email_id=emailTo.email_id)
        justKeepFirstItem(list)


def justKeepFirstItem(list):
    for idx, item in enumerate(list):
        if (idx >= 1):
            item.delete()



from enron.models import Email,ToEmail,CcEmail,BccEmail

def run():
    drop_table()

def drop_table():
    print("delete all date")
    Email.objects.all().delete()
    ToEmail.objects.all().delete()
    CcEmail.objects.all().delete()
    BccEmail.objects.all().delete()




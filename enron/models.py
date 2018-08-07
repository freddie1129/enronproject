from django.db import models
from scripts.emailconst import mailConstant

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class StaffName(models.Model):
    name = models.CharField(max_length=64,primary_key=True)
    aliasName = models.CharField(blank=True,null=True,default=None, max_length=64)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Enron Staff"
        verbose_name_plural = "Enron Staffs"


class Aliasf(models.Model):
    staff = models.ForeignKey(StaffName, on_delete=models.CASCADE)
    emailAddress = models.CharField(max_length=64)
    type = models.CharField(blank=True, null=True,default=None,max_length=16)
    number = models.IntegerField(default=0)
    isTrust = models.BooleanField(default=True)

    def __str__(self):
        return self.emailAddress

class Alias(models.Model):
        staff = models.ForeignKey(StaffName, on_delete=models.CASCADE)
        emailAddress = models.CharField(max_length=64)
        isTrust = models.BooleanField(default=True)

        def __str__(self):
            return self.emailAddress



class StaffEmail(models.Model):
    emailAddress = models.CharField(max_length=64)
    staffName = models.ForeignKey(StaffName, on_delete=models.CASCADE)
    type = models.CharField(default=mailConstant.alias_type_intrusted, max_length=16)

    def __str__(self):
        return self.staffName + ":" + self.emailAddress

    class Meta:
        verbose_name = "Enron Staff Email Address"
        verbose_name_plural = "Enron Staff Email Addresses"


class Email(models.Model):
    emailId = models.CharField(max_length=100,primary_key=True)
    time = models.DateTimeField()
    fromAddress = models.CharField(max_length=200)
    staffName = models.CharField(max_length=64)
    subject = models.CharField(max_length=512)
    content = models.TextField();
    path = models.CharField(max_length=128);

    def __str__(self):
        return self.emailId

    class Meta:
        verbose_name = "Sended Email"
        verbose_name_plural = "Sended Emails"


class RawEmail(models.Model):
    e_id = models.CharField(max_length=100,primary_key=True)
    e_date = models.TextField(blank=True, null=True, default=None)
    e_from = models.TextField(blank=True, null=True, default=None)
    e_to = models.TextField(blank=True, null=True, default=None)
    e_subject = models.TextField(blank=True, null=True, default=None)
    e_cc = models.TextField(blank=True, null=True, default=None)
    e_mime = models.TextField(blank=True, null=True, default=None)
    e_type = models.TextField(blank=True, null=True, default=None)
    e_encoding = models.TextField(blank=True, null=True, default=None)
    e_bcc = models.TextField(blank=True, null=True, default=None)
    e_x_from = models.TextField(blank=True, null=True, default=None)
    e_x_to = models.TextField(blank=True, null=True, default=None)
    e_x_cc = models.TextField(blank=True, null=True, default=None)
    e_x_bcc = models.TextField(blank=True, null=True, default=None)
    e_x_folder = models.TextField(blank=True, null=True, default=None)
    e_x_origin = models.TextField(blank=True, null=True, default=None)
    e_x_filename =  models.TextField(blank=True, null=True, default=None)
    e_content =  models.TextField(blank=True, null=True, default=None)
    e_path = models.CharField(max_length=128,blank=True, null=True, default=None)

    def __str__(self):
        return self.emailId



class ToEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    staffNameFrom = models.CharField(max_length=32)
    receiverAddress = models.CharField(max_length=200)
    staffName = models.CharField(max_length=32)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)
    emailType = models.IntegerField(default=mailConstant.email_type_unset)

    def __str__(self):
        return self.emailId

    class Meta:
        verbose_name = "Received Email"
        verbose_name_plural = "Received Emails"

class ToEmailNew(models.Model):
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)
    senderAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    senderName = models.ForeignKey(StaffName, blank=True, null=True,related_name ='sender', default=None, on_delete=models.CASCADE)
    receiverName = models.ForeignKey(StaffName, blank = True, null=True, related_name ='receiver', default=None, on_delete=models.CASCADE)
    emailType = models.IntegerField(default=mailConstant.email_type_unset)

    def __str__(self):
        return self.emailId_id

    class Meta:
        verbose_name = "Received Email"
        verbose_name_plural = "Received Emails"


class CcEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    staffNameFrom = models.ForeignKey(StaffName, verbose_name='staffNameFrom', related_name='CcEmailFrom', on_delete=models.CASCADE)
    receiverAddress = models.CharField(max_length=200)
    staffName = models.ForeignKey(StaffName, verbose_name='staffName', related_name='CcEmail', on_delete=models.CASCADE)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId

    class Meta:
        verbose_name = "CC Received Email"
        verbose_name_plural = "CC Received Emails"

class CcEmailNew(models.Model):
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)
    senderAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    senderName = models.ForeignKey(StaffName, blank=True, null=True,related_name ='ccnewsender', default=None, on_delete=models.CASCADE)
    receiverName = models.ForeignKey(StaffName, blank = True, null=True, related_name ='ccnewreceiver', default=None, on_delete=models.CASCADE)
    emailType = models.IntegerField(default=mailConstant.email_type_unset)

    def __str__(self):
        return self.emailId_id

    class Meta:
        verbose_name = "CC Received Email"
        verbose_name_plural = "CC Received Emails"


class BccEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    staffNameFrom = models.ForeignKey(StaffName, verbose_name='staffNameFrom', related_name='BccEmailFrom', on_delete=models.CASCADE)
    receiverAddress = models.CharField(max_length=200)
    staffName = models.ForeignKey(StaffName, verbose_name='staffName', related_name='BccEmail', on_delete=models.CASCADE)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId

    class Meta:
        verbose_name = "BCC Received Email"
        verbose_name_plural = "CC Received Emails"

class BccEmailNew(models.Model):
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)
    senderAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    senderName = models.ForeignKey(StaffName, blank=True, null=True,related_name ='bccnewsender', default=None, on_delete=models.CASCADE)
    receiverName = models.ForeignKey(StaffName, blank = True, null=True, related_name ='bccnewreceiver', default=None, on_delete=models.CASCADE)
    emailType = models.IntegerField(default=mailConstant.email_type_unset)

    def __str__(self):
        return self.emailId_id

    class Meta:
        verbose_name = "BCC Received Email"
        verbose_name_plural = "CC Received Emails"


class Sender(models.Model):
    sender = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return '{0} ({1})'.format(self.sender, self.number)


    class Meta:
        verbose_name = "Sender Email Address"
        verbose_name_plural = "Sender Email Addresses"

class ReceiverTo(models.Model):
    name = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.number)


    class Meta:
        verbose_name = "Receiver Email Address"
        verbose_name_plural = "Receiver Email Addresses"


class ReceiverCC(models.Model):
    name = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.number)

    class Meta:
        verbose_name = "CC Receiver Email Address"
        verbose_name_plural = "CC Receiver Email Addresses"


class ReceiverBCC(models.Model):
    name = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.number)

    class Meta:
        verbose_name = "BCC Receiver Email Address"
        verbose_name_plural = "BCC Receiver Email Addresses"


class EmailWithAlias(models.Model):
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)
    staffName = models.CharField(max_length=64)

    def __str__(self):
        return '{0} ({1})'.format(self.emailId, self.staffName)

    class Meta:
        verbose_name = "Email With Alias"
        verbose_name_plural = "Email With Alias"


class EmailWithStaff(models.Model):
    emailId = models.OneToOneField(Email, verbose_name='emailId', on_delete=models.CASCADE, primary_key=True)
    staffName = models.ForeignKey(StaffName, verbose_name='staffName', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} ({1})'.format(self.emailId, self.staffName)

    class Meta:
        verbose_name = "Email With Staff Name"
        verbose_name_plural = "Email With Staff Name"


class AnalysisResult(models.Model):
    item = models.CharField(max_length=64,primary_key=True)
    itemDes = models.CharField(max_length=64)
    itemNumber = models.IntegerField()

    def __str__(self):
        return '{0}:{1}:{2}'.format(self.item, self.itemDes,self.itemNumber)

    class Meta:
        verbose_name = "Analysis Result"
        verbose_name_plural = "Analysis Result"

class TestClassResult(models.Model):
    item = models.CharField(max_length=64)

    def __str__(self):
        return self.item


class StaCommunication(models.Model):
    staffName1 = models.ForeignKey(StaffName, blank = True, null=True, related_name ='staff1', default=None, on_delete=models.CASCADE)
    staffName2 = models.ForeignKey(StaffName, blank = True, null=True, related_name ='staff2', default=None, on_delete=models.CASCADE)
    toNumber = models.IntegerField(default=0)
    ccNumber = models.IntegerField(default=0)
    bccNumber = models.IntegerField(default=0)
    record = models.TextField()

    def __str__(self):
        return self.record

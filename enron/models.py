from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_textadd = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)




class Email(models.Model):

    emailId = models.CharField(max_length=100,primary_key=True)
    time = models.DateTimeField()
    fromAddress = models.CharField(max_length=200)
    subject = models.CharField(max_length=512)
    content = models.TextField();
    path = models.CharField(max_length=128);

    def __str__(self):
        return self.emailId

    class Meta:
        verbose_name = "Sended Email"
        verbose_name_plural = "Sended Emails"

class EmailWithAlias(models.Model):
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)
    staffName = models.CharField(max_length=64)

    def __str__(self):
        return '{0} ({1})'.format(self.emailId, self.staffName)

    class Meta:
        verbose_name = "Email With Alias"
        verbose_name_plural = "Email With Alias"

class ToEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId

    class Meta:
        verbose_name = "Received Email"
        verbose_name_plural = "Received Emails"

class CcEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId

    class Meta:
        verbose_name = "CC Received Email"
        verbose_name_plural = "CC Received Emails"

class BccEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId


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



class StaffName(models.Model):
    name = models.CharField(max_length=64,primary_key=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Enron Staff"
        verbose_name_plural = "Enron Staffs"



class StaffEmail(models.Model):
    emailAddress = models.CharField(max_length=64)
    staffName = models.ForeignKey(StaffName, on_delete=models.CASCADE)

    def __str__(self):
        return self.staffName + ":" + self.emailAddress

    class Meta:
        verbose_name = "Enron Staff Email Address"
        verbose_name_plural = "Enron Staff Email Addresses"

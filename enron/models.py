from django.db import models

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
        default_permissions=('view')

class ToEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId

    class Meta:
        verbose_name = "Received Email"
        verbose_name_plural = "Received Emails"
        default_permissions = ('view')

class CcEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId

    class Meta:
        verbose_name = "CC Received Email"
        verbose_name_plural = "CC Received Emails"
        default_permissions = ('view')




class BccEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId


    class Meta:
        verbose_name = "BCC Received Email"
        verbose_name_plural = "CC Received Emails"
        default_permissions = ('view')

class Sender(models.Model):
    sender = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return '{0} ({1})'.format(self.sender, self.number)


    class Meta:
        verbose_name = "Sender Email Address"
        verbose_name_plural = "Sender Email Addresses"
        default_permissions = ('view')

class ReceiverTo(models.Model):
    name = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.number)


    class Meta:
        verbose_name = "Receiver Email Address"
        verbose_name_plural = "Receiver Email Addresses"
        default_permissions = ('view')


class ReceiverCC(models.Model):
    name = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.number)


    class Meta:
        verbose_name = "CC Receiver Email Address"
        verbose_name_plural = "CC Receiver Email Addresses"
        default_permissions = ('view')


class ReceiverBCC(models.Model):
    name = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.number)


    class Meta:
        verbose_name = "BCC Receiver Email Address"
        verbose_name_plural = "BCC Receiver Email Addresses"
        default_permissions = ('view')



class StaffName(models.Model):
    name = models.CharField(max_length=64,primary_key=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Enron Staff"
        verbose_name_plural = "Enron Staffs"
        default_permissions = ('view')



class StaffEmail(models.Model):
    emailAddress = models.CharField(max_length=64)
    staffName = models.ForeignKey(StaffName, on_delete=models.CASCADE)

    def __str__(self):
        return self.staffName + ":" + self.emailAddress

    class Meta:
        verbose_name = "Enron Staff Email Address"
        verbose_name_plural = "Enron Staff Email Addresses"
        default_permissions = ('view')

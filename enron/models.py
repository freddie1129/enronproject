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
        return self.emailId + " " + self.fromAddress + "---->"

class ToEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId + " " + self.fromAddress + "---->" + self.receiverAddress

class CcEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId + " " + self.fromAddress + "---->" + self.receiverAddress


class BccEmail(models.Model):
    fromAddress = models.CharField(max_length=200)
    receiverAddress = models.CharField(max_length=200)
    emailId = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return self.emailId + " " + self.fromAddress + "---->" + self.receiverAddress


class Sender(models.Model):
    sender = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return self.sender


class ReceiverTo(models.Model):
    name = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return self.name



class ReceiverCC(models.Model):
    name = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return self.name

class ReceiverBCC(models.Model):
    name = models.CharField(max_length=128)
    number = models.BigIntegerField()

    def __str__(self):
        return self.name

class StaffName(models.Model):
    name = models.CharField(max_length=64,primary_key=True)
    def __str__(self):
        return self.staffname


class StaffEmail(models.Model):
    emailAddress = models.CharField(max_length=64)
    staffName = models.ForeignKey(StaffName, on_delete=models.CASCADE)

    def __str__(self):
        return self.staffname + ":" + self.emailaddress
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



class PersonAnalysis(models.Model):
    name = models.CharField(max_length=64,primary_key=True)
    #name = models.CharField(blank=True,null=True,default=None, max_length=64)
    #staff = models.ForeignKey(StaffName, on_delete=models.CASCADE)
    type = models.CharField(blank=True,null=True,default=None, max_length=64)
    diversity = models.FloatField(blank=True,null=True)
    density = models.FloatField(blank=True,null=True)
    ratio = models.FloatField(blank=True,null=True)
    time_ratio = models .FloatField(blank=True,null=True)
    sentiment = models.FloatField(blank=True,null=True)
    topic_change = models.FloatField(blank=True,null=True)
    relax_level = models.FloatField(blank=True,null=True)

    mails_to_core = models.TextField(blank=True, null=True, default=None)
    mails_to_core_send = models.TextField(blank=True, null=True, default=None)
    mails_to_core_receive = models.TextField(blank=True, null=True, default=None)
    mails_to_ext_send = models.TextField(blank=True, null=True, default=None)
    mails_to_ext_receive = models.TextField(blank=True, null=True, default=None)
    staff_to_core = models.TextField(blank=True, null=True, default=None)
    staff_to_core_send = models.TextField(blank=True, null=True, default=None)
    staff_to_core_receive = models.TextField(blank=True, null=True, default=None)

    mails_cc_core = models.TextField(blank=True, null=True, default=None)
    mails_cc_core_send = models.TextField(blank=True, null=True, default=None)
    mails_cc_core_receive = models.TextField(blank=True, null=True, default=None)
    mails_cc_ext_send = models.TextField(blank=True, null=True, default=None)
    mails_cc_ext_receive = models.TextField(blank=True, null=True, default=None)
    staff_cc_core = models.TextField(blank=True, null=True, default=None)
    staff_cc_core_send = models.TextField(blank=True, null=True, default=None)
    staff_cc_core_receive = models.TextField(blank=True, null=True, default=None)

    mails_bcc_core = models.TextField(blank=True, null=True, default=None)
    mails_bcc_core_send = models.TextField(blank=True, null=True, default=None)
    mails_bcc_core_receive = models.TextField(blank=True, null=True, default=None)
    mails_bcc_ext_send = models.TextField(blank=True, null=True, default=None)
    mails_bcc_ext_receive = models.TextField(blank=True, null=True, default=None)
    staff_bcc_core = models.TextField(blank=True, null=True, default=None)
    staff_bcc_core_send = models.TextField(blank=True, null=True, default=None)
    staff_bcc_core_receive = models.TextField(blank=True, null=True, default=None)


class Person(models.Model):
    name = models.CharField(blank=True,null=True,default=None, max_length=64)
    type = models.CharField(blank=True,null=True,default=None, max_length=64)
    diversity = models.FloatField(blank=True,null=True)
    density = models.FloatField(blank=True,null=True)
    ratio = models.FloatField(blank=True,null=True)
    time_ratio = models .FloatField(blank=True,null=True)
    sentiment = models.FloatField(blank=True,null=True)
    topic_change = models.FloatField(blank=True,null=True)
    relax_level = models.FloatField(blank=True,null=True,default=None)
    stress_level = models.FloatField(blank=True, null=True,default=None)
    scale_level = models.FloatField(blank=True, null=True,default=None)
    senti_level = models.FloatField(blank=True, null=True,default=None)



    time_divider = models.DateTimeField(blank=True,null=True)
    divider_value = models.FloatField(blank=True,null=True)


    mails_to_core = models.TextField(blank=True, null=True, default=None)
    mails_to_core_send = models.TextField(blank=True, null=True, default=None)
    mails_to_core_receive = models.TextField(blank=True, null=True, default=None)
    mails_to_core_self = models.TextField(blank=True, null=True, default=None)
    mails_to_ext_send = models.TextField(blank=True, null=True, default=None)
    mails_to_ext_receive = models.TextField(blank=True, null=True, default=None)

    staff_to_core = models.TextField(blank=True, null=True, default=None)
    staff_to_core_send = models.TextField(blank=True, null=True, default=None)
    staff_to_core_receive = models.TextField(blank=True, null=True, default=None)

    mails_cc_core = models.TextField(blank=True, null=True, default=None)
    mails_cc_core_send = models.TextField(blank=True, null=True, default=None)
    mails_cc_core_receive = models.TextField(blank=True, null=True, default=None)
    mails_cc_ext_send = models.TextField(blank=True, null=True, default=None)
    mails_cc_ext_receive = models.TextField(blank=True, null=True, default=None)
    staff_cc_core = models.TextField(blank=True, null=True, default=None)
    staff_cc_core_send = models.TextField(blank=True, null=True, default=None)
    staff_cc_core_receive = models.TextField(blank=True, null=True, default=None)

    mails_bcc_core = models.TextField(blank=True, null=True, default=None)
    mails_bcc_core_send = models.TextField(blank=True, null=True, default=None)
    mails_bcc_core_receive = models.TextField(blank=True, null=True, default=None)
    mails_bcc_ext_send = models.TextField(blank=True, null=True, default=None)
    mails_bcc_ext_receive = models.TextField(blank=True, null=True, default=None)
    staff_bcc_core = models.TextField(blank=True, null=True, default=None)
    staff_bcc_core_send = models.TextField(blank=True, null=True, default=None)
    staff_bcc_core_receive = models.TextField(blank=True, null=True, default=None)





class StaffAnalysis(models.Model):
    name = models.CharField(max_length=64,primary_key=True)
    diversity = models.FloatField(blank=True,null=True)
    density = models.FloatField(blank=True,null=True)
    ratio = models.FloatField(blank=True,null=True)
    time_ratio = models .FloatField(blank=True,null=True)
    sentiment = models.FloatField(blank=True,null=True)
    topic_change = models.FloatField(blank=True,null=True)
    relax_level = models.FloatField(blank=True,null=True)
    stress_level = models.FloatField(blank=True,null=True)

    mails_to_core_total = models.TextField(blank=True, null=True, default=None)
    mails_to_core_total_len = models.IntegerField(blank=True, null=True, default=0)
    mails_to_core_send = models.TextField(blank=True, null=True, default=None)
    mails_to_core_send_len = models.IntegerField(blank=True, null=True, default=0)
    mails_to_core_receive = models.TextField(blank=True, null=True, default=None)
    mails_to_core_receive_len = models.IntegerField(blank=True, null=True, default=0)
    mails_to_ext_send = models.TextField(blank=True, null=True, default=None)
    mails_to_ext_send_len = models.IntegerField(blank=True, null=True, default=0)
    mails_to_ext_receive = models.TextField(blank=True, null=True, default=None)
    mails_to_ext_receive_len = models.IntegerField(blank=True, null=True, default=0)

    mails_to_core_contact_total = models.TextField(blank=True, null=True, default=None)
    mails_to_core_contact_total_len = models.IntegerField(blank=True, null=True, default=0)
    mails_to_core_contact_send = models.TextField(blank=True, null=True, default=None)
    mails_to_core_contact_send_len = models.IntegerField(blank=True, null=True, default=0)
    mails_to_ext_contact_receive = models.TextField(blank=True, null=True, default=None)
    mails_to_ext_contact_receive_len = models.IntegerField(blank=True, null=True, default=0)

    mails_cc_core_total = models.TextField(blank=True, null=True, default=None)
    mails_cc_core_total_len = models.IntegerField(blank=True, null=True, default=0)
    mails_cc_core_send = models.TextField(blank=True, null=True, default=None)
    mails_cc_core_send_len = models.IntegerField(blank=True, null=True, default=0)
    mails_cc_core_receive = models.TextField(blank=True, null=True, default=None)
    mails_cc_core_receive_len = models.IntegerField(blank=True, null=True, default=0)
    mails_cc_ext_send = models.TextField(blank=True, null=True, default=None)
    mails_cc_ext_send_len = models.IntegerField(blank=True, null=True, default=0)
    mails_cc_ext_receive = models.TextField(blank=True, null=True, default=None)
    mails_cc_ext_receive_len = models.IntegerField(blank=True, null=True, default=0)

    mails_cc_core_contact_total = models.TextField(blank=True, null=True, default=None)
    mails_cc_core_contact_total_len = models.IntegerField(blank=True, null=True, default=0)
    mails_cc_core_contact_send = models.TextField(blank=True, null=True, default=None)
    mails_cc_core_contact_send_len = models.IntegerField(blank=True, null=True, default=0)
    mails_cc_ext_contact_receive = models.TextField(blank=True, null=True, default=None)
    mails_cc_ext_contact_receive_len = models.IntegerField(blank=True, null=True, default=0)

    mails_bcc_core_total = models.TextField(blank=True, null=True, default=None)
    mails_bcc_core_total_len = models.IntegerField(blank=True, null=True, default=0)
    mails_bcc_core_send = models.TextField(blank=True, null=True, default=None)
    mails_bcc_core_send_len = models.IntegerField(blank=True, null=True, default=0)
    mails_bcc_core_receive = models.TextField(blank=True, null=True, default=None)
    mails_bcc_core_receive_len = models.IntegerField(blank=True, null=True, default=0)
    mails_bcc_ext_send = models.TextField(blank=True, null=True, default=None)
    mails_bcc_ext_send_len = models.IntegerField(blank=True, null=True, default=0)
    mails_bcc_ext_receive = models.TextField(blank=True, null=True, default=None)
    mails_bcc_ext_receive_len = models.IntegerField(blank=True, null=True, default=0)

    mails_bcc_core_contact_total = models.TextField(blank=True, null=True, default=None)
    mails_bcc_core_contact_total_len = models.IntegerField(blank=True, null=True, default=0)
    mails_bcc_core_contact_send = models.TextField(blank=True, null=True, default=None)
    mails_bcc_core_contact_send_len = models.IntegerField(blank=True, null=True, default=0)
    mails_bcc_ext_contact_receive = models.TextField(blank=True, null=True, default=None)
    mails_bcc_ext_contact_receive_len = models.IntegerField(blank=True, null=True, default=0)










    # mails sent by this staff, including the mails to external person
    #mailsfrom = models.TextField(blank=True, null=True, default=None)
    #mailsfromLen = models.IntegerField(blank=True, null=True, default=0)
    #staff_from = models.TextField(blank=True, null=True, default=None)
    #staff_from_len = models.IntegerField(blank=True, null=True, default=0)

    # mails sent to the core staffs by this staff
    #mailsto = models.TextField(blank=True, null=True, default=None)
    #mailstoLen = models.IntegerField(blank=True, null=True, default=0)
    #to_staff_to = models.TextField(blank=True, null=True, default=None)
    #to_staff_to_len = models.IntegerField(blank=True, null=True, default=0)

    # mails sent cc to the core staffs by this staff
    #mailscc = models.TextField(blank=True, null=True, default=None)
    #mailsccLen = models.IntegerField(blank=True, null=True, default=0)
    #staff_cc = models.TextField(blank=True, null=True, default=None)
    #staff_cc_len = models.IntegerField(blank=True, null=True, default=0)


    # mails sent bcc to the core staffs by this staff
    #mailsbcc = models.TextField(blank=True, null=True, default=None)
    #mailsbccLen = models.IntegerField(blank=True, null=True, default=0)
    #staff_bcc = models.TextField(blank=True, null=True, default=None)
    #staff_bcc_len = models.IntegerField(blank=True, null=True, default=0)

    # total mails to, cc, bcc
    #totalmails = models.TextField(blank=True, null=True, default=None)
    #totalmailsLen = models.IntegerField(blank=True, null=True, default=0)
    #total_staff = models.TextField(blank=True, null=True, default=None)
    #total_staff_len = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name


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

import json
from django.core.serializers.json import DjangoJSONEncoder
class JsonSerializable(object):
    def toJson(self):
        return json.dumps(self.__dict__, cls=DjangoJSONEncoder)

    def __repr__(self):
        return self.toJson()




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
    e_sender_name = models.CharField(max_length=128,blank=True, null=True, default=None)

    def __str__(self):
        return self.e_id

class RawCoreEmail(models.Model):
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
    e_sender_name = models.CharField(max_length=128,blank=True, null=True, default=None)


    def __str__(self):
        return self.e_id




class RawEmailSmall(models.Model):
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
        return self.e_id

class RawEmailBackup(models.Model):
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
        return self.e_id


class ResultAddress(models.Model):
    address = models.CharField(max_length=128, primary_key=True)
    sendNumber = models.IntegerField(default=0)
    receiveToNumber = models.IntegerField(default=0)
    receiveCcNumber = models.IntegerField(default=0)
    receiveBccNumber = models.IntegerField(default=0)

    def __str__(self):
        return self.address

class ResultAddressCore(models.Model):
    address = models.CharField(max_length=128, primary_key=True)
    sendNumber = models.IntegerField(default=0)
    receiveToNumber = models.IntegerField(default=0)
    receiveCcNumber = models.IntegerField(default=0)
    receiveBccNumber = models.IntegerField(default=0)

    def __str__(self):
        return self.address

class RawEmailFrom(models.Model):
    e_id =  models.CharField(max_length=100,primary_key=True)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_subject = models.CharField(blank=True, null=True, default=None,max_length=1000)
    e_content =  models.TextField(blank=True, null=True, default=None)
    e_path = models.CharField(blank=True, null=True, default=None,max_length=200)
    relax_level = models.IntegerField(blank=True, null=True,default=None)
    stress_level = models.IntegerField(blank=True, null=True,default=None)
    scale_level = models.IntegerField(blank=True, null=True,default=None)
    senti_level = models.IntegerField(blank=True, null=True,default=None)


    e_sender_name = models.CharField(max_length=128,blank=True, null=True, default=None)

    def __str__(self):
        return "{0} From {1}".format(self.e_id, self.e_from)


class RawEmailFromCore(models.Model):
    e_id =  models.CharField(max_length=100,primary_key=True)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_subject = models.CharField(blank=True, null=True, default=None,max_length=1000)
    e_content =  models.TextField(blank=True, null=True, default=None)
    e_path = models.CharField(blank=True, null=True, default=None,max_length=200)
    relax_level = models.IntegerField(blank=True, null=True)
    stress_level = models.IntegerField(blank=True, null=True)
    e_from_name = models.CharField(blank=True,null=True, max_length=64)

    def __str__(self):
        return "{0} From {1}".format(self.e_id, self.e_from)



# email from core staff to external person
class RawEmailFromExternal(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(blank=True,null=True, max_length=128)
    e_to_name = models.CharField(blank=True,null=True, max_length=128)

    def __str__(self):
        return "{0}-->{1}".format(self.e_from_name, self.e_to_name)


# email from core staff to external person
class RawEmailToExternal(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(blank=True,null=True, max_length=128)
    e_to_name = models.CharField(blank=True,null=True, max_length=128)

    def __str__(self):
        return "{0}-->{1}".format(self.e_from_name, self.e_to_name)

class RawEmailCcExternal(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(blank=True,null=True, max_length=128)
    e_to_name = models.CharField(blank=True,null=True, max_length=128)

    def __str__(self):
        return "{0}-->{1}".format(self.e_from_name, self.e_to_name)

class RawEmailBccExternal(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(blank=True,null=True, max_length=128)
    e_to_name = models.CharField(blank=True,null=True, max_length=128)

    def __str__(self):
        return "{0}-->{1}".format(self.e_from_name, self.e_to_name)



class RawEmailTo(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(max_length=128,blank=True, null=True, default=None)
    e_to_name = models.CharField(max_length=128,blank=True, null=True, default=None)




    def __str__(self):
        return "{0} {1}-->{2}".format(self.e_id, self.e_from, self.e_to)


class RawEmailToCore(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(blank=True,null=True, max_length=128)
    e_to_name = models.CharField(blank=True,null=True, max_length=128)

    def __str__(self):
        return "{0}-->{1}".format(self.e_from_name, self.e_to_name)


class RawEmailCc(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to_name = models.CharField(max_length=128, blank=True, null=True, default=None)

    def __str__(self):
        return "{0} {1}-->{2}".format(self.e_id, self.e_from, self.e_to)


class RawEmailCcCore(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to_name = models.CharField(max_length=128, blank=True, null=True, default=None)

    def __str__(self):
        return "{0} {1}-->{2}".format(self.e_id, self.e_from, self.e_to)


class RawEmailBCc(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to_name = models.CharField(max_length=128, blank=True, null=True, default=None)

    def __str__(self):
        return "{0} {1}-->{2}".format(self.e_id, self.e_from, self.e_to)


class RawEmailBCcCore(models.Model):
    e_id =  models.ForeignKey(RawEmailFrom, on_delete=models.CASCADE)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    def __str__(self):
        return "{0} {1}-->{2}".format(self.e_id, self.e_from, self.e_to)

class RawComm(models.Model):
    staff_a = models.ForeignKey(StaffName, blank = True, null=True, related_name ='staff_a', default=None, on_delete=models.CASCADE)
    staff_b = models.ForeignKey(StaffName, blank = True, null=True, related_name ='staff_b', default=None, on_delete=models.CASCADE)
    number_a_b = models.IntegerField(default=0)
    number_b_a = models.IntegerField(default=0)
    record = models.TextField()

    def __str__(self):
        return self.record


class EmailBrief(models.Model):
    e_id = models.CharField(max_length=100,primary_key=True)
    e_date = models.DateTimeField()
    e_from = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_to = models.CharField(max_length=128, blank=True, null=True, default=None)
    e_from_name = models.CharField(blank=True, null=True, max_length=128)
    e_to_name = models.CharField(blank=True, null=True, max_length=128)
    e_type = models.CharField(blank=True, null=True, max_length=32)


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

class StaStaffEmailData():
    def __init__(self,name,senderNum,receiveToNum,receiveCcNum,receiveBccNum,detail):
        self.name = name
        self.senderNum = senderNum
        self.receiveToNum = receiveToNum
        self.receiveCcNum = receiveCcNum
        self.receiveBccNum = receiveBccNum
        self.total = senderNum + receiveToNum + receiveCcNum + receiveBccNum
        self.addressList = detail
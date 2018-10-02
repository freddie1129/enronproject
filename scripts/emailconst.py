
class mailConstant:
    cons_maildir = '/root/maildir/'

    result_received_email_number = "(Table:ToEmail, received Email) email number"
    result_received_email_number_from_enron_group = "received email number from staffs inside enron group"
    result_received_email_number_from_external = "received email number from person outside enron group"
    result_received_email_number_to_enron_group = "received email number to enron group"
    result_received_email_number_to_external = "received email number to person outside enron group"
    result_received_email_number_between_enron_group = "received email number between enron group"

    email_type_unset = -1
    email_type_unknow = 0
    email_type_from = 1
    email_type_to = 2
    email_type_between = 3

    alias_type_trusted = "trusted"
    alias_type_intrusted = "intrusted"


    e_type_c_to_c = "c_to_c" #core to core mails
    e_type_c_to_e = "c_to_e" #core to external mails
    e_type_c_cc_c = "c_cc_c" #core cc core mails
    e_type_c_cc_e = "c_cc_e" #core cc external mails
    e_type_c_bcc_c = "c_bcc_c" #core bcc core mails
    e_type_c_bcc_e = "c_bcc_e" #core bcc external mails





    string_unknown = "unkonwn"


    analysis_type_training = "training"
    analysis_type_testing = "testing"

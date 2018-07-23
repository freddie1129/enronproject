from .maillib import analysis_mail
import datetime

def run():
    print("Start at: {0}".format(str(datetime.datetime.now())))
    analysis_mail()
    print("End at: {0}".format(str(datetime.datetime.now())))


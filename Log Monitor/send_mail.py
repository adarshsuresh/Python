from datetime import datetime
GLOBAL_TOTAL=0

def sendmail(msg):
    global GLOBAL_TOTAL
    GLOBAL_TOTAL+=1
    print("""\
    ##########################################
    ##          SERVER ALERT                ##
    ##                                      ##
    ## received: {date:%Y-%m-%d %H:%M:%S.%f}##
    ## total_alerts: {total:7d}             ##
    ##########################################
    {msg}""".format(date=datetime.now(),total=GLOBAL_TOTAL,msg=msg))
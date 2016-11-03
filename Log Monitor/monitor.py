import  json
from argparse import ArgumentParser
from send_mail import sendmail
from log_monitor import Monitor


def myformat(mydict):
    """
    My formatter for the current context
    :param mydict: Dict having current context of log
    :return: Formatted String
    """
    return json.dumps(mydict, indent=4, sort_keys=True)


def main():
    p = ArgumentParser()
    p.add_argument("list_log_file", help="List of log files that should be monitered.")
    args=p.parse_args()
    args.list_log_file=args.list_log_file.split(',')
    print(args)
    monitor_list=[]
    for file in args.list_log_file:
        monitor=Monitor(file,{"ERROR":[sendmail]},10,{"ERROR":myformat})
        monitor.start()
        monitor_list.append(monitor)
    for thread in monitor_list:
        thread.join()

if __name__ == '__main__':
    main()
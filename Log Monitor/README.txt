python3 monitor.py "list of files to monitor sperated by ','"

Two main classes take care of the monitoring part.
Monitor
Log_Context


Monitor: Each montor class is a separate thread which runs on start().
         In monitor a log file is read and if no new line is found the thread is put to sleep.
         Each line of log is sent to the log context class and it retuns the Level name of log.
         If the level name matches the return call spefied , then the return call is triggered by the Monitor.
         Return call is a list so a list more than one retun call can be triggered for the same level.

Log_Context : Log context stores the log file in two different format. It stores the last log files in list for a particular
              size called store count . It also stores the data of each Level and each module to that perticular count too.
              It takes a formatter dictionary which can format this dictionary to the required format for different types of
              levels.The default one is to print the last 10 lines of log.

              Dict Format:
              {Level_name:{"module_name":[(date,msg),(date,msg)]}}

monitor.py takes a list of files seperated by ',' and starts one monitor class for each file.
While call ing the monitor class we have to provide the logfile, return calls, store count and also the format of the msg.
In my sample i used send mail as the return call for ERROR and formater called myformat for ERROR . IF a return call for
WARNING should be added just add the a value {"WARNING":[newreturncall]} to the return call dict.We have to remeber that Return call
is list so more than one return call can be trigerred for a level.




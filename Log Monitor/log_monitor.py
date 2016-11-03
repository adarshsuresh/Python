from logcontext import Log_Context
import time,threading

class Monitor(threading.Thread):
    def __init__(self,log_file,returncall,storecount=10,format={}):
        """

        :param log_file: File to be read
        :param returncall: A dict containing the levelname and return call for that
        :param storecount: Data that should be stored in the the log context
        :param format: A dict containg format function for Each level name
        """
        super(Monitor, self).__init__()
        self.log_file=log_file
        self.log_context=Log_Context(format,storecount)
        self.returncall=returncall

    def run(self):
        self.read_log()

    def read_log(self):
        """
        Reads the log file if new line is available else it sleeps.
        When a new line is read it is sent to process log.
        :return: None
        """
        with open(self.log_file, "r") as log:
            while 1:
                where = log.tell()
                line = log.readline()
                if not line:
                    time.sleep(1)
                    log.seek(where)
                else:
                    self.process_log(line)

    def process_log(self,log):
        """
        Each line of log is seperated and sent to the log context object which stores the context of the current log
        :param log: Each line of log. (str)
        :return:
        """
        level_name=self.log_context.insert(log)
        if level_name in self.returncall:
            for returncall in self.returncall[level_name]:
                returncall(self.log_context.format_output(level_name))

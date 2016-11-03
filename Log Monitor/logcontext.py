class Log_Context(object):
    def __init__(self,format={},store_count=10):
        """

        :param format: A dict containg format function for Each level name
        :param store_count: Amount of data that should be stored in the the log context
        """
        self.log_context={}
        self.format=format
        self.last_log=[]
        self.store_count=store_count

    def insert(self,log):
        """
        Inserts the log to last_log and also to log context depending on the store_count
        :param log: A line of log
        :return: Level name
        """
        date, module_name, level_name, msg = self.split_log(log)
        if len(self.last_log)>self.store_count:
            self.last_log.pop()
        self.last_log.append(log)
        if level_name in self.log_context:
            level_context = self.log_context[level_name]
            if module_name in level_context:
                if len(level_context) >self.store_count:
                    level_context.pop()
                level_context[module_name].append((date, msg))
            else:
                level_context[module_name] = [(date, msg)]
        else:
            self.log_context[level_name] = {}
            self.log_context[level_name][module_name] = [(date, msg)]
        return  level_name

    def split_log(self, log):
        """
        Default Split log formatter which splits the log line to date, module name , msg and level name
        :param log: Each line of log
        :return: date , module name m level name , msg seperated is sent to the file
        """
        start = log.find('[')
        end = log.find(']')
        date = log[start + 1:end]
        log = log[end + 1:]
        start = log.find('[')
        end = log.find(']')
        module_name = log[start + 1:end]
        log = log[end + 1:]
        start = log.find('[')
        end = log.find(']')
        level_name = log[start + 1:end]
        msg = log[end + 1:]
        return date, module_name, level_name, msg

    def format_output(self,formatcall=None):
        """
        Default format caller which prints the last 10 line of log or the formats to the call which is specified for it.
        :param formatcall: The format function call.
        :return: A formatted string
        """
        if formatcall == None or formatcall not in self.format:
            return "".join(self.last_log)
        else:
            return self.format[formatcall](self.log_context)
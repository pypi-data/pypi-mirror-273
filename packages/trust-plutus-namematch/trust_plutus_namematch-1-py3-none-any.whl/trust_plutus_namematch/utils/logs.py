from loga import Loga

# all setup values are optional
loga = Loga(
    facility="Fund Name Match",  # name of program logging the message
    do_print=True,  # print each log to console
    do_write=True,  # write each log to file
    logfile="./logs/mylog.txt",  # custom path to logfile
    truncation=1000,  # longest possible value in extra data
    # private_data={"api_key"}  # set of sensitive args/kwargs
)
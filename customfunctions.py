import time

#Setting up a way to display time in human readable format
intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])
#***********************************************************

# This is a simple timestamp function, created so each call would have a current timestamp
def timestamp():
    ts = time.strftime("%x %X", time.localtime())
    return ("<" + ts + "> ")
#******************************************************************************************


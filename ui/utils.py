show_time_units = False
def convertMillis(millis):
    if millis is None:
        return "unknown"
    seconds = round(int((millis) % 60), 2)
    minutes = round(int((millis/(60)) % 60), 2)
    hours = round(int((millis/(60*60)) % 24), 2)
    s = ""
    u = None
    if hours > 0:
        s = s+'{:02d}:'.format(hours)
        u = "h"
    if minutes > 0:
        s = '{}{:02d}:'.format(s, minutes)
        if u is None:
            u = "m"
    if u is None:
        u = "s"
    s = '{}{:02d}'.format(s, seconds)
    if show_time_units:
        return s+u
    else:
        return s
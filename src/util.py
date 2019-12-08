def sec_to_str(sec):
    return str(int(sec/60/60)) + ":" + str(int(sec/60%60)) + ":" + str(int(sec%60))
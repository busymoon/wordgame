# coding: utf-8


def common_chars( wroot,off0,wcmp,off1,flags):
    if off0==len(wroot) or off1==len(wcmp):
        return 0
    if wroot[off0]==wcmp[off1]:
        flags[off1] = 1
        return 1+common_chars(wroot, off0+1, wcmp, off1+1,flags)
    else:
        k = flags[off1]
        flags[off1] = 0
        x1 = common_chars(wroot, off0, wcmp, off1+1,flags)
        flags[off1] = k
        x2 = common_chars(wroot, off0+1, wcmp, off1,flags)
        return max(x1,x2)
def wrap_chars(wcmp, flags):
    return " ".join([c if f==0 else "<font color='blue'>{}</font>".format(c) for c,f in zip(wcmp,flags)])


# w1="otheor"
# w2="mother"
# flags=[0 for _ in range(len(w2))]
# print(common_chars(w1,0,w2,0,flags))
# print(str(flags))
# print(wrap_chars(w2,flags))

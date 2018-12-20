import sys
import os
import numpy as np
from datetime import date
import reg_proc

td = date.today()
def gen1(arg1):
    a = int(10*np.random.rand())

    if arg1 == '0':
        wrd1 = "今天是" + "%s"%td.year + "年" + "%s"%td.month + "月" + "%s"%td.day + "日, ";
    else:
        if a > 5:
            wrd1 = "驚聞"
        elif a < 5:
            wrd1 = "說到"
        wrd1 += arg1 + ", "

    return wrd1


def gen2(myissue):
    a = int(10*np.random.rand())

    if a > 5:
        wrd2 = "就不得不提"
    else:
        wrd2 = "令人想起了"
    if myissue == '0':
        a = int(96*np.random.rand())
        tmpStr = reg_proc.parse("xiyou-chs.txt")
        wrd2 += "西游记中的《" + tmpStr[a] + "》. ";
    else:
        wrd2 += myissue + ". "

    return wrd2


def main():
    w1, w2 = gen1(sys.argv[1]), gen2(sys.argv[2])
    print(w1 + w2 + "今年下半年，中美合拍的電影西遊記即將正式開機，我繼續扮演美猴王孫悟空，我會用美猴王藝術，努力創造一個正能量的讓海內外觀眾滿意的新的熒幕形象，文體兩開花，弘揚中華文化！")

if __name__ == "__main__":
    main()

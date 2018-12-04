import re
import sys
import os
import numpy as np
import matplotlib.pyplot as plt


def parse(filename, sepa_loc=r"=(\d*)ms", IF_PRINT=False):
    # parsinf function.
    file_annot = open(filename, 'r')
    pingtimes = []
    labels = []

    sample_idx = 0  # line num counter for input file
    for line in file_annot:

        # print("ORIGINAL TEXT: " + line)
        searchObj = re.search(sepa_loc, line, re.M | re.I | re.S)
        pingfail = re.search("Request timed out.", line, re.M | re.I | re.S)
        if searchObj:
            sample_idx = sample_idx + 1
            tmpStr = searchObj.group()
            tmpStr = tmpStr[1:-2]  # save ping time exclusively, the brackets
            tmpList = tmpStr.split(",")

            for k in range(len(tmpList)):
                tmpList[k] = int(tmpList[k])
            # tmpList = tuple(tmpList) # so it wont be manipulated later

            if IF_PRINT:
                print("Try:%d\t\t" % sample_idx, " PING= ", tmpList[0], "ms")
            pingtimes.append(tmpList)
            labels.append(1)
        else:
            if pingfail:
                sample_idx = sample_idx + 1
                if IF_PRINT: print("Try:%d\t\t" % sample_idx, " PING= ", "--- NO ENTRY ---")
                # pingtimes.append()  # no target
                labels.append(0)
            else:
                pass
    return pingtimes, labels


def main():
    sitename, pingnum = sys.argv[1], sys.argv[2]

    CURRENT_PATH = os.getcwd()

    os.system('ping ' + sitename + ' -n ' + pingnum +
              ' > ' + CURRENT_PATH + '/pingdata.txt')
    pingdata, success = parse("./pingdata.txt", r"=(\d*)ms", True)

    plt.figure(figsize=(14, 4))
    plt.subplot(1, 3, 1)
    plt.scatter(np.arange(len(pingdata)), pingdata)
    plt.grid(True)
    plt.title("Ping %s (ms)"%sitename)
    plt.subplot(1, 3, 2)
    plt.boxplot(np.array(pingdata))
    plt.grid(True)
    plt.title("Ping time box plot")
    plt.subplot(1, 3, 3)
    labels = ["Pinged", "Time Out"]
    plt.pie([sum(success), len(success) - sum(success)], labels=labels, autopct='%1.1f%%')
    plt.title("Ping success %3.2f %%" % (100*sum(success)/len(success)))

    plt.show()

    # os.system("del pingdata.txt")
    print("Test complete. Temp file remains.")


if __name__ == "__main__":
    main()

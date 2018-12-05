
import re
import sys
import os
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
                print("Try:%d\t\t" % sample_idx, " PING: ", tmpList)
            pingtimes.append(tmpList)
            labels.append(1)
        else:
            if pingfail:
                sample_idx = sample_idx + 1
                print("Try:%d\t\t" % sample_idx, " PING: ", "--- NO ENTRY ---")
                # pingtimes.append()  # no target
                labels.append(0)
            else:
                pass
    return pingtimes, labels
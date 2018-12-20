import re, os, sys

import re, os, sys

def parse(filename, IF_PRINT=False, sepa_loc=r"[ ][\u4e00-\u9fa5]*[ ][\u4e00-\u9fa5]*", ):
    # parsinf function.
    file_annot = open(filename, 'r',encoding="utf8")
    textList = [];
    sample_idx = 0  # line num counter for input file
    for line in file_annot:
        # print("ORIGINAL TEXT: " + line)
        searchObj = re.search(sepa_loc, line, re.M | re.I | re.S)
        pingfail = re.search("Request timed out.", line, re.M | re.I | re.S)
        if searchObj:
            sample_idx = sample_idx + 1
            tmpStr = searchObj.group()
            textList.append(tmpStr);
            # tmpStr = tmpStr[1:-2]  # save ping time exclusively, the brackets
            
    if IF_PRINT: print(textList)
    return textList

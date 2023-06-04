# -*- coding: utf-8 -*-

import numpy as np

from twr_main import *

class dataAna:
    def __init__(self, truePos, filePath):
        self.posResult = []
        self.truePos = truePos
        self.filePath = filePath

    def loadData(self):
        f = open(self.filePath, "r")
        lines = f.readlines()
        posResult = np.zeros((len(lines), 2))
        for idx, line in enumerate(lines):
            _, _, _, location_x, location_y = twr_main(line)
            posResult[idx, 0] = location_x
            posResult[idx, 1] = location_y
        f.close()
        self.posResult = posResult


# 配置参数1
truePos = np.array([[3.0, 4.0]])
dir = 'logData/'
log_file = '123.txt'
filePath = dir + log_file

data1 = dataAna(truePos, filePath)
data1.loadData()
print(data1.posResult)










# -*- coding: utf-8 -*-

import numpy as np

from twr_main import *

class dataAna:
    def __init__(self, truePos, filePath):
        self.posResult = 0
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

    def calRMS(self):
        return np.mean(np.linalg.norm(self.posResult-self.truePos, axis=1))

# 配置参数1
truePos = np.array([[-5.98, -15.07]])
dir = 'logData/'
log_file = '123.txt'
filePath = dir + log_file

data1 = dataAna(truePos, filePath)
data1.loadData()
rms = data1.calRMS()
print(data1.posResult)
print(rms)









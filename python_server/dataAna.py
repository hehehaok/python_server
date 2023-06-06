# -*- coding: utf-8 -*-

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
truePosA = np.array([[0, 1.40]])
dir = 'logData/'
log_file = 'posA.txt'
filePathA = dir + log_file

dataA = dataAna(truePosA, filePathA)
dataA.loadData()
rmsA = dataA.calRMS()
print(dataA.posResult)
print(rmsA)


# 配置参数2
# truePosB = np.array([[1.4, 2.94]])
# dir = 'logData/'
# log_file = 'posB.txt'
# filePathB = dir + log_file
#
# dataB = dataAna(truePosB, filePathB)
# dataB.loadData()
# rmsB = dataB.calRMS()
# print(dataB.posResult)
# print(rmsB)

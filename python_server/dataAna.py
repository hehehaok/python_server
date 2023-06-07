# -*- coding: utf-8 -*-
import time
from twr_main import *

class dataAna:
    def __init__(self, truePos, filePath):
        self.posResult = 0
        self.truePos = truePos
        self.filePath = filePath

    def calPos2D(self):
        f = open(self.filePath, "r")
        lines = f.readlines()
        posResult = np.zeros((len(lines), 2))
        for idx, line in enumerate(lines):
            error_flag, result_dic = Process_String_Before_Udp(line)
            if error_flag == 0:
                Info = BP_Process_String(result_dic)
                if Info['count'] > 3:
                    tril2d = Trilateration()
                    tril2d.setDistances(Info['distance'])
                    tril2d.setAnthorCoor(Info['anthor'])
                    posResult[idx, :] = tril2d.trilaterate2D()
        f.close()
        self.posResult = posResult

    def calPos2DInTyler(self):
        f = open(self.filePath, "r")
        lines = f.readlines()
        posResult = np.zeros((len(lines), 2))
        for idx, line in enumerate(lines):
            error_flag, result_dic = Process_String_Before_Udp(line)
            if error_flag == 0:
                Info = BP_Process_String(result_dic)
                if Info['count'] > 3:
                    tril2d = Trilateration()
                    tril2d.setDistances(Info['distance'])
                    tril2d.setAnthorCoor(Info['anthor'])
                    result = tril2d.trilaterate2D()
                    posResult[idx, :] = tril2d.trilaterate2D_2(iterations=10, refPos0=np.array(result))
        f.close()
        self.posResult = posResult

    def calPos3D(self):
        f = open(self.filePath, "r")
        lines = f.readlines()
        posResult = np.zeros((len(lines), 3))
        for idx, line in enumerate(lines):
            error_flag, result_dic = Process_String_Before_Udp(line)
            if error_flag == 0:
                Info = BP_Process_String(result_dic)
                if Info['count'] > 3:
                    tril3d = Trilateration()
                    tril3d.setDistances(Info['distance'])
                    tril3d.setAnthorCoor(Info['anthor'])
                    posResult[idx, :] = tril3d.trilaterate3D()
        f.close()
        self.posResult = posResult

    def calPos3DInTyler(self):
        f = open(self.filePath, "r")
        lines = f.readlines()
        posResult = np.zeros((len(lines), 3))
        for idx, line in enumerate(lines):
            error_flag, result_dic = Process_String_Before_Udp(line)
            if error_flag == 0:
                Info = BP_Process_String(result_dic)
                if Info['count'] > 3:
                    tril3d = Trilateration()
                    tril3d.setDistances(Info['distance'])
                    tril3d.setAnthorCoor(Info['anthor'])
                    result = tril3d.trilaterate3D()
                    posResult[idx, :] = tril3d.trilaterate3D_2(iterations=5, refPos0=np.array(result))
        f.close()
        self.posResult = posResult

    def calRMS(self):
        idx = np.where(self.posResult[:] == [0, 0])[0]
        posResult = np.delete(self.posResult, idx, axis=0)
        return np.mean(np.linalg.norm(posResult-self.truePos, axis=1))

# 配置参数1
truePosA = np.array([[0, 1.40]])
dir = 'logData/'
log_file = 'posA.txt'
filePathA = dir + log_file

dataA = dataAna(truePosA, filePathA)
start_time = time.time()
dataA.calPos2D()
# dataA.calPos2DInTyler()
end_time = time.time()
print("程序运行时间为：", end_time - start_time, "秒")
rmsA = dataA.calRMS()
# print(dataA.posResult)
print(rmsA)


# 配置参数2
# truePosB = np.array([[1.4, 2.94]])
# dir = 'logData/'
# log_file = 'posB.txt'
# filePathB = dir + log_file
#
# dataB = dataAna(truePosB, filePathB)
# dataB.calPos2D()
# # dataB.calPos2DInTyler()
# rmsB = dataB.calRMS()
# print(dataB.posResult)
# print(rmsB)

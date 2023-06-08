# -*- coding: utf-8 -*-
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
                    posResult[idx, :] = tril2d.trilaterate2D_2(iterations=5, refPos0=np.array(result))
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
                    # result = tril3d.trilaterate3D()
                    result = np.array([4.0, 5.0, 1.08])[:,None]
                    posResult[idx, :] = tril3d.trilaterate3D_2(iterations=20, refPos0=np.array(result))
        f.close()
        self.posResult = posResult

    def calRMS2D(self):
        idx = np.where(self.posResult[:] == [0, 0, 0])[0]
        posResult = np.delete(self.posResult, idx, axis=0)
        return np.mean(np.linalg.norm((posResult-self.truePos)[:,:-1], axis=1))

    def calRMS3D(self):
        idx = np.where(self.posResult[:] == [0, 0, 0])[0]
        posResult = np.delete(self.posResult, idx, axis=0)
        return np.mean(np.linalg.norm(posResult-self.truePos, axis=1))

    def scatterPlot2D(self):
        plt.figure(100)
        plt.rcParams['font.family'] = ['SimHei']
        p1 = plt.scatter(self.truePos[0,0], self.truePos[0,1], c='red', s=40)
        p2 = plt.scatter(self.posResult[:,0], self.posResult[:,1], c='blue', s=30)
        plt.legend([p1, p2], ['真实位置', '定位结果'])
        plt.xlabel('x/米')
        plt.ylabel('y/米')
        plt.title('2维定位结果散点图')
        plt.show()
        return

    def scatterPlot3D(self):
        plt.figure(200)
        ax = plt.axes(projection='3d')
        plt.rcParams['font.family'] = ['SimHei']
        p1 = ax.scatter3D(self.truePos[0,0], self.truePos[0,1], self.truePos[0,2], c='red', s=40)
        p2 = ax.scatter3D(self.posResult[:,0], self.posResult[:,1], self.posResult[:,2], c='blue', s=30)
        plt.legend([p1, p2], ['真实位置', '定位结果'])
        plt.title('3维定位结果散点图')
        plt.show()
        return
# 配置参数1
# truePosA = np.array([[0, 1.40]])
# dir = 'logData/'
# log_file = 'posA.txt'
# filePathA = dir + log_file

# dataA = dataAna(truePosA, filePathA)
# # start_time = time.time()
# dataA.calPos2D()
# # dataA.calPos2DInTyler()
# # end_time = time.time()
# # print("程序运行时间为：", end_time - start_time, "秒")
# rmsA = dataA.calRMS()
# # print(dataA.posResult)
# print(rmsA)


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

# 配置参数3
# truePosA2 = np.array([[4.0, 5.0, 1.08]])
# dir = 'logData/'
# log_file = 'posA2.txt'
# filePathA2 = dir + log_file
#
# dataA2 = dataAna(truePosA2, filePathA2)
# dataA2.calPos3D()
# dataA2.scatterPlot2D()
# # dataA2.calPos3DInTyler()
# rmsA2 = dataA2.calRMS2D()
# print(dataA2.posResult)
# print(rmsA2)

# 配置参数4
# truePosE1 = np.array([[0, 5.0, 1.08]])
# dir = 'logData/'
# log_file = 'posE1.txt'
# filePathE1 = dir + log_file
#
# dataE1 = dataAna(truePosE1, filePathE1)
# dataE1.calPos2D()
# dataE1.scatterPlot2D()
# # dataA2.calPos3DInTyler()
# # rmsE1 = dataE1.calRMS2D()
# print(dataE1.posResult)
# # print(rmsE1)

# 配置参数5
truePosF1 = np.array([[0, 0, 1.08]])
dir = 'logData/'
log_file = 'posF1.txt'
filePathF1 = dir + log_file

dataF1 = dataAna(truePosF1, filePathF1)
dataF1.calPos2D()
dataF1.scatterPlot2D()
# dataF1.calPos3DInTyler()
# rmsF1 = dataF1.calRMS2D()
print(dataF1.posResult)
# print(rmsF1)
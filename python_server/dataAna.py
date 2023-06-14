# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from filterpy.kalman import ExtendedKalmanFilter
import numpy as np

from twr_main import *

class dataAna:
    def __init__(self, truePos, filePath):
        self.posResult = 0 # 解算位置
        self.truePos = truePos # 真实位置
        self.filePath = filePath # 数据文件路径

    def calPos(self):
        f = open(self.filePath, "r")
        lines = f.readlines()
        result = np.zeros((len(lines), 3))
        for idx, line in enumerate(lines):
            error_flag, result_dic = Process_String_Before_Udp(line)
            if error_flag == 0:
                Info = BP_Process_String(result_dic)
                trilater = Trilateration()
                trilater.setDistances(Info['distance'])
                trilater.setAnthorCoor(Info['anthor'])
                # trilater.setAnthorNlos(Info['isNlos']) # 注释掉即不去除NLOS基站
                result[idx, :] = trilater.trilaterate()
        f.close()
        self.posResult = result

    def calPosEKF(self):
        """
        静态条件二维下的EKF
        """
        # 初始化EKF
        rk = ExtendedKalmanFilter(dim_x=2, dim_z=4)
        rk.x = np.array(np.zeros((2,1)))
        rk.F = np.eye(2)
        rk.Q = np.diag([0.01, 0.01]) # 状态噪声
        rk.R = np.diag([0.01, 0.01, 0.01, 0.01]) # 观测噪声
        rk.P *= 1

        f = open(self.filePath, "r")
        lines = f.readlines()
        result = np.zeros((len(lines), 3))
        for idx, line in enumerate(lines):
            error_flag, result_dic = Process_String_Before_Udp(line)
            if error_flag == 0:
                Info = BP_Process_String(result_dic)
                rk.update(np.array(Info['distance']).T, calJacobia, calMeas)
                result[idx, 0:2] = rk.x
                rk.predict()
        f.close()
        self.posResult = result

    def calRMS2D(self):
        idx = np.where((self.posResult==np.array([0, 0, 0])).all(axis=1))[0]
        posResult = np.delete(self.posResult, idx, axis=0)
        return np.mean(np.linalg.norm((posResult-self.truePos)[:,:-1], axis=1))

    def calRMS3D(self):
        idx = np.where((self.posResult==np.array([0, 0, 0])).all(axis=1))[0]
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

    def tracePlot(self, tracePoint):
        plt.figure(300)
        plt.rcParams['font.family'] = ['SimHei']
        plt.plot(tracePoint[:, 0], tracePoint[:, 1])
        plt.plot(self.posResult[:,0], self.posResult[:,1])
        plt.legend(['真实轨迹', '定位轨迹'])
        plt.title('2维定位结果轨迹图')
        plt.show()
        return

    def scenePlot(self, tracePoint):
        anchor = np.array([[0, 10.32, 10.32, 0, 0], [0, 0, 10.01, 10.01, 0]]).T
        pillar = np.array([[1.78, 2.85, 2.85, 1.78, 1.78], [4.48, 4.48, 6.37, 6.37, 4.48]]).T
        plt.figure(400)
        plt.rcParams['font.family'] = ['SimHei']
        plt.plot(tracePoint[:, 0], tracePoint[:, 1], '-')
        plt.plot(anchor[:, 0], anchor[:, 1])
        plt.plot(pillar[:, 0], pillar[:, 1])
        plt.title('场地俯视图')
        plt.show()
        return

def calJacobia(x):
    anchor = np.array([[0,0], [10.32, 0], [10.32, 10.01], [0, 10.01]])
    xk = x[0] - anchor[:, 0]
    yk = x[1] - anchor[:, 1]
    pho = np.sqrt(xk ** 2 + yk ** 2)
    jacobiaH = np.array([xk/pho, yk/pho]).T
    return jacobiaH

def calMeas(x):
    anchor = np.array([[0,0], [10.32, 0], [10.32, 10.01], [0, 10.01]])
    xk = x[0] - anchor[:, 0]
    yk = x[1] - anchor[:, 1]
    pho = np.sqrt(xk ** 2 + yk ** 2)
    return pho[:, None]

# 配置参数A1
truePosA = np.array([[6.32, 3.2, 0]]) # 2维定位纵坐标设置为0
dir = 'logData/'
log_file = 'A1.txt'
filePathA = dir + log_file

dataA = dataAna(truePosA, filePathA)
# dataA.calPos()
dataA.calPosEKF()
rmsA = dataA.calRMS2D()
print(rmsA)
dataA.scatterPlot2D()

# 配置参数B5
# truePosA = np.array([[6.32, 3.2, 0]]) # 2维定位纵坐标设置为0
# dir = 'logData/'
# log_file = 'B5.txt'
# filePathA = dir + log_file
# tracePoint = np.array([[0.8, 3.92, 3.92, 0.8, 0.8], [3.2, 3.2, 7.61, 7.61, 3.2]]).T
#
# dataA = dataAna(truePosA, filePathA)
# dataA.calPos()
# rmsA = dataA.calRMS2D()
# print(rmsA)
# # dataA.tracePlot(tracePoint)
# dataA.scenePlot(tracePoint)
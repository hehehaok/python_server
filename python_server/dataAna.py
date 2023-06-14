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
        return result

    def calPosEKF(self):
        """
        静态条件二维下的EKF
        状态方程： Xk = [[x_k],[y_k]] = [[1,0],[0,1]]@[[x_(k-1)],[y_(k-1)]]+[[wx_(k-1)],[wy_(k-1)]]
        观测方程：4个基站到标签的距离作为观测量，参照论文[UWB Positioning System Based on LSTM Classification With Mitigated NLOS Effects]
        """
        # 初始化EKF
        rk = ExtendedKalmanFilter(dim_x=2, dim_z=4) # 状态向量的个数 观测向量的个数
        rk.x = np.array(np.ones((2,1))) # 状态向量[[x_k],[y_k]]
        rk.F = np.eye(2) # 状态转移矩阵
        rk.Q = np.diag([0.01, 0.01]) # 状态噪声
        rk.R = np.diag([0.01, 0.01, 0.01, 0.01]) # 观测噪声
        rk.P *= 0.1 # 均方误差阵

        f = open(self.filePath, "r")
        lines = f.readlines()
        result = np.zeros((len(lines), 3))
        for idx, line in enumerate(lines):
            error_flag, result_dic = Process_String_Before_Udp(line)
            if error_flag == 0:
                Info = BP_Process_String(result_dic)
                rk.update(np.array(Info['distance'])[:, None], calJacobia, calMeas)
                result[idx, 0:2] = rk.x.T
                rk.predict()
        f.close()
        self.posResult = result
        return result

    def calRMS2D(self):
        idx = np.where((self.posResult==np.array([0, 0, 0])).all(axis=1))[0]
        posResult = np.delete(self.posResult, idx, axis=0)
        return np.mean(np.linalg.norm((posResult-self.truePos)[:,:-1], axis=1))

    def calRMS3D(self):
        idx = np.where((self.posResult==np.array([0, 0, 0])).all(axis=1))[0]
        posResult = np.delete(self.posResult, idx, axis=0)
        return np.mean(np.linalg.norm(posResult-self.truePos, axis=1))

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

# 场景坐标
anchor = np.array([[0, 10.32, 10.32, 0, 0], [0, 0, 10.01, 10.01, 0]]).T # 基站坐标
pillar = np.array([[1.78, 2.85, 2.85, 1.78, 1.78], [4.48, 4.48, 6.37, 6.37, 4.48]]).T # 柱坐标


# 配置参数A1 - 二维静态
truePosA1 = np.array([[6.32, 3.2, 0]]) # 2维定位纵坐标设置为0
dir = 'logData/'
log_file = 'A1.txt'
filePathA1 = dir + log_file

dataA1 = dataAna(truePosA1, filePathA1)
posLS = dataA1.calPos()
rmsLS = dataA1.calRMS2D()
posEKF = dataA1.calPosEKF()
rmsEKF = dataA1.calRMS2D()


plt.figure(400)
plt.rcParams['font.family'] = ['SimHei']
p1 = plt.scatter(dataA1.truePos[0,0], dataA1.truePos[0,1], c='red', s=40)
p2 = plt.scatter(posLS[:,0], posLS[:,1], c='blue', s=30)
p3 = plt.scatter(posEKF[:,0], posEKF[:,1], c='green', s=30)
plt.legend([p1, p2, p3], ['真实位置', 'LS结果%.4f'%(rmsLS), 'EKF结果%.4f'%(rmsEKF)], loc='lower right')
plt.title('场地俯视图')
plt.show()



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
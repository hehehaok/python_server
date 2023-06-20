# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from filterpy.kalman import ExtendedKalmanFilter
import numpy as np
import os

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
                if result_dic['anthor_count'] != 4:
                    error_flag = 1 # 排除异常数据
            if error_flag == 0:
                Info = BP_Process_String(result_dic)
                trilater = Trilateration()
                trilater.setDistances(Info['distance'])
                trilater.setAnthorCoor(Info['anthor'])
                # trilater.setAnthorNlos(Info['isNlos']) # 注释掉即不去除NLOS基站
                result[idx, :] = trilater.trilaterate()
        f.close()
        idx = np.where((result==np.array([0, 0, 0])).all(axis=1))[0]
        posResult = np.delete(result, idx, axis=0)
        self.posResult = posResult
        return posResult

    def calPosEKF(self):
        """
        静态条件二维下的EKF
        状态方程： Xk = [[x_k],[y_k]] = [[1,0],[0,1]]@[[x_(k-1)],[y_(k-1)]]+[[wx_(k-1)],[wy_(k-1)]]
        观测方程：4个基站到标签的距离作为观测量，参照论文[UWB Positioning System Based on LSTM Classification With Mitigated NLOS Effects]
        """
        # 初始化EKF
        # rk = ExtendedKalmanFilter(dim_x=2, dim_z=4) # 状态向量的个数 观测向量的个数
        # rk.x = np.array(np.ones((2,1))) # 状态向量[[x_k],[y_k]]
        # rk.F = np.eye(2) # 状态转移矩阵
        # rk.Q = np.diag([0.01, 0.01]) # 状态噪声
        # rk.R = np.diag([0.01, 0.01, 0.01, 0.01]) # 观测噪声
        # rk.P *= 0.1 # 均方误差阵

        # 动态二维条件下的EKF
        # 初始化EKF
        rk = ExtendedKalmanFilter(dim_x=4, dim_z=4) # 状态向量的个数 观测向量的个数
        ts = 0.025 # 采样点数据间隔
        rk.x = np.array(np.ones((4,1))) # 状态向量[[x_k],[y_k],[vx_k],[vy_k]]
        rk.F = np.eye(4) + np.array([[0,0,1,0],
                                     [0,0,0,1],
                                     [0,0,0,0],
                                     [0,0,0,0]])*ts # 状态转移矩
        # rk.Q = (np.array([[ts/2,0],[0,ts/2],[1,0],[0,1]])*ts)@np.diag([0.01, 0.01]) # 状态噪声
        rk.Q = np.diag([0.01, 0.01, 0.01, 0.01]) # 状态噪声
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
                result[idx, 0:2] = rk.x.T[0,0:2]
                rk.predict()
        f.close()
        self.posResult = result
        return result

    def calRMS_static(self, axis):
        # 输出参数axis表示计算哪几个维度上的RMS
        # 如axis=[0,1,2]表示计算3个维度上的均方误差 axis=[2]表示仅计算z轴上的均方误差
        return np.mean(np.linalg.norm((self.posResult-self.truePos)[:,axis], axis=1))

    def calRMS_dynamic(self, tracePoint, axis):
        # 输出参数axis表示计算哪几个维度上的RMS
        # 如axis=[0,1,2]表示计算3个维度上的均方误差 axis=[2]表示仅计算z轴上的均方误差
        return np.mean(np.linalg.norm((self.posResult-tracePoint)[:,axis], axis=1))

def calJacobia(x):
    anchor = np.array([[0,0], [10.32, 0], [10.32, 10.01], [0, 10.01]])
    xk = x[0] - anchor[:, 0]
    yk = x[1] - anchor[:, 1]
    pho = np.sqrt(xk ** 2 + yk ** 2)
    H1 = np.array([xk/pho, yk/pho]).T
    jacobiaH = np.zeros((4,4))
    jacobiaH[:,0:2] = H1
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
anchor3D = np.array([[0, 10.32, 10.32, 0, 0],
                     [0, 0, 10.01, 10.01, 0],
                     [1.27, 0.2, 2.34, 1.535, 1.27]]).T # 基站坐标

# 图像保存路径
figPath = 'dataFig'
if not os.path.exists(figPath):
    os.makedirs(figPath)
figPath = figPath + '/'
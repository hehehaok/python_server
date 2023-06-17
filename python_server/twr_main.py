# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:27:12 2021

@author: www.51uwb.cn
"""
import time  # 引入time模块
import re
from Coordinate_process import BP_Process_String
import sys
import numpy as np


class Trilateration:
    def __init__(self):
        self.position = []
        self.distances = []
        self.result = 0

    def trilaterate2D(self):
        A = []
        B = []
        result = np.zeros((3,))
        r2_n = np.sum([x**2 for x in self.position[-1, :]])
        for idx in range(np.shape(self.position)[0]-1):
            x_coefficient = self.position[-1][0] - self.position[idx][0]
            y_coefficient = self.position[-1][1] - self.position[idx][1]
            r2_idx = np.sum([x**2 for x in self.position[idx, :]])
            b = 1 / 2 * (self.distances[idx] ** 2 - self.distances[-1] ** 2 + r2_n - r2_idx)
            A.append([x_coefficient, y_coefficient])
            B.append([b])
        B = np.array(B)
        A_pseudo = np.linalg.pinv(A)
        self.result = np.dot(A_pseudo, B)
        result[0:2] = self.result.T[0,:] # 2维定位返回纵坐标为0
        return result

    def trilaterate3D(self):
        '''
        在UWB基站架设的时候，需要特别拉开z轴的高度差，以确保在z轴上的精确度。
        '''
        A = []
        B = []
        result = np.zeros((3,))
        r2_n = np.sum([x**2 for x in self.position[-1, :]])
        for idx in range(np.shape(self.position)[0]-1):
            x_coefficient = self.position[-1][0] - self.position[idx][0]
            y_coefficient = self.position[-1][1] - self.position[idx][1]
            z_coefficient = self.position[-1][2] - self.position[idx][2]
            r2_idx = np.sum([x**2 for x in self.position[idx][:]])
            b = 1 / 2 * (self.distances[idx] ** 2 - self.distances[3] ** 2 + r2_n - r2_idx)
            A.append([x_coefficient, y_coefficient, z_coefficient])
            B.append([b])
        B = np.array(B)
        A_pseudo = np.linalg.pinv(A)
        self.result = np.dot(A_pseudo, B)
        result = self.result.T[0,:]
        return result

    def trilaterate2DInTyler(self, iterations=10, refPos0=None):
        if refPos0 is None:
            refPos = np.ones((2,))
            # 如果使用零矩阵，则在(0,0)处的基站和refPos的距离r0为0
            # A[idx, :] = -((position[idx, :] - refPos) / r0)的结果为nan
        else:
            assert np.shape(refPos0) == (3,)
            refPos = refPos0[:,:-1]
        result = np.zeros((3,))
        position = self.position[:,:-1]
        numRx = np.shape(position)[0]
        A = np.zeros((numRx, 2))
        b = np.zeros((numRx, 1))
        for i in range(iterations):
            for idx in range(numRx):
                r0 = np.linalg.norm(position[idx, :] - refPos)
                b[idx, 0] = self.distances[idx] - r0
                A[idx, :] = -((position[idx, :] - refPos) / r0)
            x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
            refPos = refPos + x.T
            if np.linalg.norm(x) < 1.0e-4:
                break
        refPos = np.squeeze(refPos, axis=0)
        self.result = refPos
        result[0:2] = refPos
        return result

    def trilaterate3DInTyler(self, iterations=10, refPos0=None):
        if refPos0 is None:
            refPos = np.zeros((3,))
        else:
            assert np.shape(refPos0) == (3,)
            refPos = refPos0
        result = np.zeros((3,))
        position = self.position
        numRx = np.shape(position)[0]
        A = np.zeros((numRx, 3))
        b = np.zeros((numRx, 1))
        for i in range(iterations):
            for idx in range(numRx):
                r0 = np.linalg.norm(position[idx, :] - refPos)
                b[idx, 0] = self.distances[idx] - r0
                A[idx, :] = -((position[idx, :] - refPos) / r0)
            x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
            refPos = refPos + x.T
            if np.linalg.norm(x) < 1.0e-4:
                break
        refPos = np.squeeze(refPos, axis=0)
        self.result = refPos
        result = refPos
        return result

    def trilaterate(self):
        count = np.shape(self.position)[0] # 根据可用基站个数选择定位算法
        # 选择2维定位还是3维定位
        if np.sum(np.abs(self.position[:,2])) == 0: #基站纵坐标全设置为0表示使用2维定位
            if count < 2:
                self.result = np.zeros((3,))
            elif count == 2:
                self.result = self.trilaterate2DInTyler()
            else:
                self.result = self.trilaterate2D()
        else: # 否则使用三维定位
            if count < 3:
                self.result = np.zeros((3,))
            elif count == 3:
                self.result = self.trilaterate3DInTyler()
            else:
                self.result = self.trilaterate3D()
        return self.result

    def setDistances(self, distances):
        self.distances = distances

    def setAnthorCoor(self, Anthor_Node_Configure):
        self.position = np.zeros((len(Anthor_Node_Configure),3))
        for index in range(len(Anthor_Node_Configure)):
            self.position[index][0] = Anthor_Node_Configure[index][0]
            self.position[index][1] = Anthor_Node_Configure[index][1]
            self.position[index][2] = Anthor_Node_Configure[index][2]

    def setAnthorNlos(self, isNlos):
        nlosIdx = np.where(isNlos)[0]
        # nlosIdx = [2]
        if(len(nlosIdx)):
            self.position = np.delete(self.position, nlosIdx, axis=0)
            for idx,i in enumerate(nlosIdx):
                del self.distances[i]
                nlosIdx[idx+1:] = [m-1 for m in nlosIdx[idx+1:]]

# &&&:80$000A:20$0001:A1B1:0011:0#0002:A2B2:0022:0#0003:A3B3:0033:0#0004:A4B4:0044:0$CRC####
# 根据约定格式提取数据包里的各个信息
def bphero_dispose(string):
    result_dict = {'tag': 0x1005, 'seq': 7, 'time': 1234, 'anthor_count': 4,'anthor': []} # tag-标签短地址 seq-数据包中的seqNumber anthor_count-基站个数

    # 数据包以&&& 开头
    res = re.findall(r'&&&', string)
    flag = 1
    if len(res) > 0:
        # step1 print message length,ex 76
        temp_string = string.split("$")[0]  # &&&:80
        data_len = int(temp_string.split(":")[1], 16)

        # tag info
        temp_string = string.split("$")[1]  # 000A:20
        tag_id = int(temp_string.split(":")[0], 16)  # 000A
        tag_seq = int(temp_string.split(":")[1], 16)  # 20
        # print("标签ID: %02X  Seq: %X" % (tag_id, tag_seq))
        result_dict['tag'] = tag_id
        result_dict['seq'] = tag_seq

        # anthor info
        temp_string = string.split("$")[2]  # 0001:A1B1:0011:0#0002:A2B2:0022:0#0003:A3B3:0033:0#0004:A4B4:0044:0
        anthor_count = len(temp_string.split('#'))
        result_dict['anthor_count'] = anthor_count

        for index in range(anthor_count):
            anthor_info = temp_string.split('#')[index]  # 0001:A1B1:0011:0
            anthor_id = int(anthor_info.split(":")[0], 16)
            anthor_dist = 0.01*int(anthor_info.split(":")[1], 16)   # convert to cm
            # print("Anthor%d Distance = %0.2f m"% (index+1, anthor_dist))
            anthor_rssi = -0.01*int(anthor_info.split(":")[2], 16)
            anthor_isnlos = int(anthor_info.split(":")[3], 16)
            result_dict['anthor'].append([anthor_id, anthor_dist, anthor_rssi, anthor_isnlos])
        flag = 0
    return flag, result_dict

def Compute_Location(Input_Data):
    Info = BP_Process_String(Input_Data)
    # print(Info)
    trilater = Trilateration()
    trilater.setDistances(Info['distance'])
    trilater.setAnthorCoor(Info['anthor'])
    trilater.setAnthorNlos(Info['isNlos'])
    result = trilater.trilaterate()
    result_flag = 1
    print("x = %0.2f, y = %0.2f, z = %0.2f" % (result[0], result[1], result[2]))
    return result_flag, Info['seq'], Info['tag'], Info['isNlos'], result[0], result[1], result[2]


# step1 处理接收来的数据包
def Process_String_Before_Udp(NewString):
    try:
        error_flag, result_dic = bphero_dispose(NewString) # error_flag=0表示数据读取正常
    except:
        print('error')
        return 1,0
    return error_flag, result_dic

def twr_main(input_string):
    print(input_string)
    error_flag, result_dic = Process_String_Before_Udp(input_string)
    if error_flag == 0:
        [location_flag, location_seq, location_addr, isNlos, location_x, location_y, location_z] = Compute_Location(result_dic)
        return location_flag, location_seq, location_addr, isNlos, location_x, location_y, location_z
    return 0, 0, 0, 0, 0, 0, 0

# test code ==============================
'''
x = 0.93
y = 0.72
import math
dis1 = math.sqrt((x-0)*(x-0) + (y-0)*(y-0))
print(dis1)
dis2 = math.sqrt((x-10)*(x-10) + (y-0)*(y-0))
print(dis2)
dis3 = math.sqrt((x-10)*(x-10) + (y-10)*(y-10))
print(dis3)
dis4 = math.sqrt((x-0)*(x-0) + (y-10)*(y-10))
print(dis4)

# s = '&&&:80$000A:20$0001:%04X:0011:0#0002:%04X:0022:0#0003:%04X:0033:0#0004:%04X:0044:0$CRC####' % (int(dis1*100), int(dis2*100),int(dis3*100),int(dis4*100))
s = '&&&:20$0005:CF$0001:007C:1C00:1#0002:00D8:303A:0#0003:00'
# s = '&&&:20$0005:EB$0001:007F:2046:1#'
print(s)
twr_main(s)
'''
'''
x = 3.2
y = 1
z = 2
import math
dis1 = math.sqrt((x-0)*(x-0) + (y-0)*(y-0) + (z-0)*(z-0))
print(dis1)
dis2 = math.sqrt((x-10)*(x-10) + (y-0)*(y-0) + (z-1)*(z-1))
print(dis2)
dis3 = math.sqrt((x-10)*(x-10) + (y-10)*(y-10) + (z-2)*(z-2))
print(dis3)
dis4 = math.sqrt((x-0)*(x-0) + (y-10)*(y-10) + (z-3)*(z-3))
print(dis4)

s = '&&&:80$000A:20$0001:%04X:0011:1#0002:%04X:0022:0#0003:%04X:0033:0#0004:%04X:0044:0$CRC####' % (int(dis1*100), int(dis2*100), int(dis3*100), int(dis4*100))
print(s)
twr_main(s)
'''
# test code end ===========================


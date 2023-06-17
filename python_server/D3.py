import matplotlib.pyplot as plt
import numpy as np

from dataAna import *
# 使用前记得检查globalvar中基站坐标是使用的二维基站坐标还是三维基站坐标

# 配置参数D3 - 三维动态 绕柱走
truePosD3 = np.array([[0, 3.2, 0]]) # 2维定位纵坐标设置为0
dir = 'logData/'
log_file = 'D3.txt'
filePathD3 = dir + log_file

# 读取数据文件 定位解算
dataD3 = dataAna(truePosD3, filePathD3)
posLS = dataD3.calPos()

# 真实轨迹点
trace = np.array([[0.8, 3.92, 3.92, 0.8, 0.8],
                  [3.2, 3.2, 7.61, 7.61, 3.2],
                  [1.1, 1.1, 1.1, 1.1, 1.1]]).T #柱轨迹坐标
tracex = np.array([0.8, 3.92])
tracey = np.array([3.2, 7.61])

tracePoint = np.zeros(np.shape(posLS))
for ii in range(np.shape(posLS)[0]):
    tracePoint[ii, 0] = tracex[np.argmin(np.abs(posLS[ii, 0]-tracex))]
    tracePoint[ii, 1] = tracey[np.argmin(np.abs(posLS[ii, 1]-tracey))]
    tracePoint[ii, 2] = 1.1


# posEKF = dataD3.calPosEKF()
# rmsEKF = dataD3.calRMS2D()

# 画图
fig = plt.figure(400)
plt.rcParams['font.family'] = ['SimHei']
ax = plt.gca()

# 场地基站
for ii in range(4):
    plt.scatter(anchor[ii, 0], anchor[ii, 1], c='green')
    plt.text(anchor[ii, 0]+0.15, anchor[ii, 1], '基站%d'%(ii+1),
             fontsize=10, color="black", style="italic", weight="light",
             verticalalignment='center', horizontalalignment='left', rotation=0)

# 场地柱子
pillar_x = pillar[0:2, 0]
pillar_y1 = pillar[0, 1]
pillar_y2 = pillar[2, 1]
plt.fill_between(pillar_x, pillar_y1, pillar_y2, color = 'black', alpha = 0.2)
plt.text(pillar[0, 0] + 0.23, pillar[0, 1]+0.9, '石柱',
         fontsize=10, color="black", style="italic", weight="light",
         verticalalignment='center', horizontalalignment='left', rotation=0)

# 真实位置和定位结果
plt.plot(tracePoint[:,0], tracePoint[:,1],
         color='red', linestyle='-', linewidth=2.5, label= "真实轨迹")
plt.plot(posLS[:,0], posLS[:,1], color='blue', marker='.', label= "定位结果")
plt.legend(loc='center right', borderaxespad=0)
# p3 = plt.scatter(posEKF[:,0], posEKF[:,1], c='green', s=30)
# plt.legend([p1, p2, p3], ['真实位置', 'LS结果%.4f'%(rmsLS), 'EKF结果%.4f'%(rmsEKF)], loc='lower right')


# 去除右边和上边的边框
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# 坐标轴标题，显示网格，图标题
plt.xlabel('X[m]')
plt.ylabel('Y[m]')
plt.grid('on')
rmsLS = dataD3.calRMS_dynamic(tracePoint=tracePoint, axis=[0,1,2])
rmsLSxy = dataD3.calRMS_dynamic(tracePoint=tracePoint, axis=[0,1])
rmsLSz = dataD3.calRMS_dynamic(tracePoint=tracePoint, axis=[2])
plt.title('场景D2定位测试图，定位结果RMS=%.4f米\n'
          '水平RMS=%.4f米,高度RMS=%.4f米'%(rmsLS, rmsLSxy, rmsLSz))
plt.show()
fig.savefig(figPath+'D3.svg',format='svg',dpi=150)#输出
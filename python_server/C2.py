import numpy as np
import matplotlib

from dataAna import *
# 使用前记得检查globalvar中基站坐标是使用的二维基站坐标还是三维基站坐标

# 配置参数C2 - 三维静态
truePosC2 = np.array([[6.32, 7.6, 1.1]]) # 2维定位纵坐标设置为0
dir = 'logData/'
log_file = 'C2.txt'
filePathC2 = dir + log_file

# 读取数据文件 定位解算
dataC2 = dataAna(truePosC2, filePathC2)
posLS = dataC2.calPos()
# posEKF = dataC2.calPosEKF()
# rmsEKF = dataC2.calRMS3D()

# 画图
fig1 = plt.figure(400)
plt.rcParams['font.family'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus']=False
ax = plt.gca()

# 场地基站
for ii in range(4):
    plt.scatter(anchor3D[ii, 0], anchor3D[ii, 1], c='green')
    plt.text(anchor3D[ii, 0]+0.15, anchor3D[ii, 1], '基站%d'%(ii+1),
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
p1 = plt.scatter(dataC2.truePos[0,0], dataC2.truePos[0,1], c='red', s=200, marker='*')
p2 = plt.scatter(posLS[:,0], posLS[:,1], c='blue', s=30)
plt.legend([p1, p2], ['真实位置', '定位结果'], loc='upper right', borderaxespad=-3)
# p3 = plt.scatter(posEKF[:,0], posEKF[:,1], c='green', s=30)
# plt.legend([p1, p2, p3], ['真实位置', 'LS结果%.4f'%(rmsLS), 'EKF结果%.4f'%(rmsEKF)], loc='lower right')

# 子图
rect1 = [0.43, 0.3, 0.35, 0.35]
axins = ax.inset_axes(rect1)
tx0 = truePosC2[0,0] - 0.02
tx1 = truePosC2[0,0] + 0.15
ty0 = truePosC2[0,1] - 0.05
ty1 = truePosC2[0,1] + 0.7
axins.axis([tx0, tx1, ty0, ty1])
axins.scatter(dataC2.truePos[0,0], dataC2.truePos[0,1], c='red', s=40, marker='*')
axins.scatter(posLS[:,0], posLS[:,1], c='blue', s=30)
axins.grid('on')


# 去除右边和上边的边框
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# 坐标轴标题，显示网格，图标题
plt.xlabel('X[m]')
plt.ylabel('Y[m]')
plt.grid('on')
rmsLS = dataC2.calRMS_static(axis=[0,1,2])
rmsLSxy = dataC2.calRMS_static(axis=[0,1])
rmsLSz = dataC2.calRMS_static(axis=[2])
plt.title('场景C1定位测试图，定位结果RMS=%.4f米\n'
          '水平RMS=%.4f米,高度RMS=%.4f米'%(rmsLS, rmsLSxy, rmsLSz))
plt.show()
fig1.savefig(figPath+'C2.svg',format='svg',dpi=150)#输出

#############################################################################################################

# # 画纵坐标的分布情况
# fig2 = plt.figure(500)
# plt.rcParams['font.family'] = ['SimHei']
# ax = plt.gca()
#
# # 场地基站(高度)
# for ii in range(4):
#     plt.scatter(0, anchor3D[ii, 2], c='green', s=100)
#     plt.text(0.15, anchor3D[ii, 2], '基站%d'%(ii+1),
#              fontsize=10, color="black", style="italic", weight="light",
#              verticalalignment='center', horizontalalignment='left', rotation=0)
#
# # 真实位置和定位结果
# p1 = plt.scatter(0, dataC2.truePos[0,2], c='red', s=200, marker='*')
# p2 = plt.scatter(np.zeros(np.shape(posLS[:,2])), posLS[:,2], c='blue', s=30)
# plt.legend([p1, p2], ['真实位置', '定位结果'], loc='upper right', borderaxespad=-3)
# # p3 = plt.scatter(posEKF[:,0], posEKF[:,1], c='green', s=30)
# # plt.legend([p1, p2, p3], ['真实位置', 'LS结果%.4f'%(rmsLS), 'EKF结果%.4f'%(rmsEKF)], loc='lower right')
#
# # 子图
# # rect1 = [0.43, 0.3, 0.35, 0.35]
# # axins = ax.inset_axes(rect1)
# # tx0 = truePosC2[0,0] - 0.02
# # tx1 = truePosC2[0,0] + 0.15
# # ty0 = truePosC2[0,1] - 0.05
# # ty1 = truePosC2[0,1] + 0.7
# # axins.axis([tx0, tx1, ty0, ty1])
# # axins.scatter(dataC2.truePos[0,0], dataC2.truePos[0,1], c='red', s=40, marker='*')
# # axins.scatter(posLS[:,0], posLS[:,1], c='blue', s=30)
# # axins.grid('on')
#
#
# # 去除右边和上边的边框
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
#
# # 坐标轴标题，显示网格，图标题
# plt.ylabel('Z[m]')
# plt.grid('on')
# plt.title('场景C1定位测试图，定位结果RMS=%.4f米'%(rmsLS))
# plt.show()
# # fig2.savefig(figPath+'C2.svg',format='svg',dpi=150)#输出
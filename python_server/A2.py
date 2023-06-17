import numpy as np

from dataAna import *
# 使用前记得检查globalvar中基站坐标是使用的二维基站坐标还是三维基站坐标
# 使用前修改setAnthorNlos中的nlosIdx，nlosIdx = np.where(isNlos)[0] -> nlosIdx = [2]
# 即手动将基站3视为NLOS基站

# 配置参数A2 - 二维静态 基站3非视距
truePosA2 = np.array([[4.72, 3.55, 0]]) # 2维定位纵坐标设置为0
dir = 'logData/'
log_file = 'A2.txt'
filePathA2 = dir + log_file

# 读取数据文件 定位解算
dataA2 = dataAna(truePosA2, filePathA2)
posLS = dataA2.calPos()
rmsLS = dataA2.calRMS_static(axis=[0,1])
# posEKF = dataA2.calPosEKF()
# rmsEKF = dataA2.calRMS2D()

# 画图
fig = plt.figure(400)
plt.rcParams['font.family'] = ['SimHei']
ax = plt.gca()
# plt.axis('equal')
# plt.axis([1.5, 10.5, -0.5, 10.5])

# 场地基站
# 基站3为NLOS基站
plt.scatter(anchor[2, 0], anchor[2, 1], c='gray')
plt.text(anchor[2, 0] + 0.15, anchor[2, 1], '基站3(NLOS)',
         fontsize=10, color="black", style="italic", weight="light",
         verticalalignment='center', horizontalalignment='left', rotation=0)
for ii in [0, 1, 3]:
    plt.scatter(anchor[ii, 0], anchor[ii, 1], c='green')
    plt.text(anchor[ii, 0]+0.15, anchor[ii, 1], '基站%d'%(ii+1),
             fontsize=10, color="black", style="italic", weight="light",
             verticalalignment='center', horizontalalignment='left', rotation=0)

# 画个人挡住基站3
human_x = np.linspace(9.5, 10.2, 2)
human_y1 = -human_x + 18
human_y2 = -human_x + 20
plt.fill_between(human_x, human_y1, human_y2, color = 'black', alpha = 0.5)
plt.text(human_x[0]+0.05, human_y1[0]+0.5, '挡板',
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
p1 = plt.scatter(dataA2.truePos[0,0], dataA2.truePos[0,1], c='red', s=200, marker='*')
p2 = plt.scatter(posLS[:,0], posLS[:,1], c='blue', s=30)
plt.legend([p1, p2], ['真实位置', '定位结果'], loc='upper right', borderaxespad=-3)
# p3 = plt.scatter(posEKF[:,0], posEKF[:,1], c='green', s=30)
# plt.legend([p1, p2, p3], ['真实位置', 'LS结果%.4f'%(rmsLS), 'EKF结果%.4f'%(rmsEKF)], loc='lower right')

# 子图
rect1 = [0.43, 0.5, 0.35, 0.35]
axins = ax.inset_axes(rect1)
tx0 = truePosA2[0,0] - 0.02
tx1 = truePosA2[0,0] + 0.12
ty0 = truePosA2[0,1] - 0.12
ty1 = truePosA2[0,1] + 0.02
axins.axis([tx0, tx1, ty0, ty1])
axins.scatter(dataA2.truePos[0,0], dataA2.truePos[0,1], c='red', s=40, marker='*')
axins.scatter(posLS[:,0], posLS[:,1], c='blue', s=30)
axins.grid('on')

# 去除右边和上边的边框
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# 坐标轴标题，显示网格，图标题
plt.xlabel('X[m]')
plt.ylabel('Y[m]')
plt.grid('on')
plt.title('场景A2定位测试图，定位结果RMS=%.4f米'%(rmsLS))
plt.show()
fig.savefig(figPath+'A2.svg',format='svg',dpi=150)#输出
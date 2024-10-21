import numpy as np

# 定义参数
np_ = 9
nlo = 360
nla = 180

# 初始化数组
vp = np.zeros((np_, nla, nlo))
vs = np.zeros((np_, nla, nlo))
rho = np.zeros((np_, nla, nlo))
bnd = np.zeros((np_, nla, nlo))
thk = np.zeros((np_, nla, nlo))
thc = np.zeros((nla, nlo))
ths = np.zeros((nla, nlo))

print(' .... reading all maps ... ')

# 读取数据
with open('crust1.vp', 'r') as f1, \
     open('crust1.vs', 'r') as f2, \
     open('crust1.rho', 'r') as f3, \
     open('crust1.bnds', 'r') as f4:
    for j in range(nla):
        for i in range(nlo):
            vp[:, j, i] = list(map(float, f1.readline().split()))
            vs[:, j, i] = list(map(float, f2.readline().split()))
            rho[:, j, i] = list(map(float, f3.readline().split()))
            bnd[:, j, i] = list(map(float, f4.readline().split()))

# 写出地图
for k in range(1, np_ + 1):
    cmap = f'map-vp{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            f.write(' '.join(f'{vp[k-1, j, i]:5.2f}' for i in range(nlo)) + '\n')

    cmap = f'map-vs{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            f.write(' '.join(f'{vs[k-1, j, i]:5.2f}' for i in range(nlo)) + '\n')

    cmap = f'map-ro{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            f.write(' '.join(f'{rho[k-1, j, i]:5.2f}' for i in range(nlo)) + '\n')

    cmap = f'map-bd{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            f.write(' '.join(f'{bnd[k-1, j, i]:7.2f}' for i in range(nlo)) + '\n')

# 计算厚度并写出
for k in range(1, 9):
    cmap = f'map-th{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            for i in range(nlo):
                thk[k-1, j, i] = -(bnd[k, j, i] - bnd[k-1, j, i])
            f.write(' '.join(f'{thk[k-1, j, i]:7.2f}' for i in range(nlo)) + '\n')

# 计算总厚度
with open('sedthk', 'w') as f1, open('crsthk', 'w') as f2:
    for j in range(nla):
        for i in range(nlo):
            ths[j, i] = thk[2, j, i] + thk[3, j, i] + thk[4, j, i]
            thc[j, i] = thk[1, j, i] + ths[j, i] + thk[5, j, i] + thk[6, j, i] + thk[7, j, i]
        f1.write(' '.join(f'{ths[j, i]:7.2f}' for i in range(nlo)) + '\n')
        f2.write(' '.join(f'{thc[j, i]:7.2f}' for i in range(nlo)) + '\n')

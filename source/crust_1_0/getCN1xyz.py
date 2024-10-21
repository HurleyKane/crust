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
    cmap = f'xyz-vp{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            flat = 90.0 - j + 0.5
            for i in range(nlo):
                flon = -180.0 + i - 0.5
                f.write(f'{flon:6.1f} {flat:6.1f} {vp[k-1, j, i]:5.2f}\n')

    cmap = f'xyz-vs{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            flat = 90.0 - j + 0.5
            for i in range(nlo):
                flon = -180.0 + i - 0.5
                f.write(f'{flon:6.1f} {flat:6.1f} {vs[k-1, j, i]:5.2f}\n')

    cmap = f'xyz-ro{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            flat = 90.0 - j + 0.5
            for i in range(nlo):
                flon = -180.0 + i - 0.5
                f.write(f'{flon:6.1f} {flat:6.1f} {rho[k-1, j, i]:5.2f}\n')

    cmap = f'xyz-bd{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            flat = 90.0 - j + 0.5
            for i in range(nlo):
                flon = -180.0 + i - 0.5
                f.write(f'{flon:6.1f} {flat:6.1f} {bnd[k-1, j, i]:7.2f}\n')

# 计算厚度并写出
for k in range(1, 9):
    cmap = f'xyz-th{k}'
    with open(cmap, 'w') as f:
        for j in range(nla):
            flat = 90.0 - j + 0.5
            for i in range(nlo):
                flon = -180.0 + i - 0.5
                thk[k-1, j, i] = -(bnd[k, j, i] - bnd[k-1, j, i])
                f.write(f'{flon:6.1f} {flat:6.1f} {thk[k-1, j, i]:7.2f}\n')

# 计算总厚度
with open('sedthk.xyz', 'w') as f1, open('crsthk.xyz', 'w') as f2:
    for j in range(nla):
        flat = 90.0 - j + 0.5
        for i in range(nlo):
            flon = -180.0 + i - 0.5
            ths[j, i] = thk[2, j, i] + thk[3, j, i] + thk[4, j, i]
            thc[j, i] = thk[1, j, i] + ths[j, i] + thk[5, j, i] + thk[6, j, i] + thk[7, j, i]
            f1.write(f'{flon:6.1f} {flat:6.1f} {ths[j, i]:7.2f}\n')
            f2.write(f'{flon:6.1f} {flat:6.1f} {thc[j, i]:7.2f}\n')

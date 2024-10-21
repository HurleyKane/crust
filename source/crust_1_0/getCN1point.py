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

while True:
    print('enter center lat, long of desired tile (q to quit)')
    input_str = input()
    
    if input_str.lower() == 'q':
        break
    
    try:
        flat, flon = map(float, input_str.split())
    except ValueError:
        print("Invalid input. Please enter valid latitude and longitude.")
        continue

    # 确保经度在 -180 到 180 之间
    if flon > 180.0:
        flon -= 360.0
    if flon < -180.0:
        flon += 360.0

    ilat = int(90 - flat + 1)
    ilon = int(180 + flon + 1)

    print(f'ilat,ilon,crustal type: {ilat:4d}, {ilon:4d}')
    print(f'topography: {bnd[0, ilat - 1, ilon - 1]:7.2f}')
    print(' layers: vp,vs,rho,bottom')

    for i in range(1, np_):
        print(f'{vp[i - 1, ilat - 1, ilon - 1]:7.2f} {vs[i - 1, ilat - 1, ilon - 1]:7.2f} {rho[i - 1, ilat - 1, ilon - 1]:7.2f} {bnd[i, ilat - 1, ilon - 1]:7.2f}')

    print(f' pn,sn,rho-mantle: {vp[8, ilat - 1, ilon - 1]:7.2f} {vs[8, ilat - 1, ilon - 1]:7.2f} {rho[8, ilat - 1, ilon - 1]:7.2f}')

import os
import numpy as np
import xarray as xr
from crust.config import get_rootPath

vp = os.path.join(get_rootPath(), "source",  'crust1.vp')
vs = os.path.join(get_rootPath(), "source",  'crust1.vs')
rho = os.path.join(get_rootPath(),"source",  'crust1.rho')
bnd = os.path.join(get_rootPath(),"source",  'crust1.bnds')

class CrustData(xr.Dataset):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    @staticmethod
    def read_data(self):
        np_ = 9
        nlo = 360
        nla = 180
        vp = np.zeros((np_,  nla, nlo))
        vs = np.zeros((np_,  nla, nlo))
        rho = np.zeros((np_, nla, nlo))
        bnd = np.zeros((np_, nla, nlo))
        with open(vp, 'r') as f1, \
             open(vs, 'r') as f2, \
             open(rho, 'r') as f3, \
             open(bnd, 'r') as f4:
            for j in range(nla):
                for i in range(nlo):
                    vp[:, j, i] = list(map(float, f1.readline().split()))
                    vs[:, j, i] = list(map(float, f2.readline().split()))
                    self.rho[:, j, i] = list(map(float, f3.readline().split()))
                    self.bnd[:, j, i] = list(map(float, f4.readline().split()))

        # 创建坐标
        layers = ["water", "ice", "upper sediments", "middle sediments", "lower sediments", "upper crust",
                    "middle crust", "lower crust", "mantle"]
        la_coords = np.arange(nla)
        lo_coords = np.arange(nlo)

        # 创建 xarray.Dataset
        dataset = xr.Dataset(
            {
                'VP': (['p', 'la', 'lo'], vp),
                'VS': (['p', 'la', 'lo'], vs),
                'RHO': (['p', 'la', 'lo'], rho),
                'BND': (['p', 'la', 'lo'], bnd)
            },
            coords={
                'p': layers,
                'lan': la_coords,
                'lon': lo_coords
            }
        )
        return CrustData(dataset)

    def one_points_query(self, lat, lon):
        if lon > 180.0:
            lon -= 360.0
        if lon < -180.0:
            lon += 360.0

        ilat = int(90 - lat + 1)
        ilon = int(180 + lon + 1)

        result = {
            'ilat': ilat,
            'ilon': ilon,
            'topography': self.bnd[0, ilat - 1, ilon - 1],
            'layers': []
        }

        for i in range(1, self.np_):
            result['layers'].append({
                'vp': self.vp[i - 1, ilat - 1, ilon - 1],
                'vs': self.vs[i - 1, ilat - 1, ilon - 1],
                'rho': self.rho[i - 1, ilat - 1, ilon - 1],
                'bottom': self.bnd[i, ilat - 1, ilon - 1]
            })

        result['pn'] = self.vp[8, ilat - 1, ilon - 1]
        result['sn'] = self.vs[8, ilat - 1, ilon - 1]
        result['rho_mantle'] = self.rho[8, ilat - 1, ilon - 1]

        return result

    def one_point_query_text(self, lat, lon):
        result = self.one_points_query(lat, lon)
        print(f'ilat,ilon,crustal type: {result["ilat"]:4d}, {result["ilon"]:4d}')
        print(f'topography: {result["topography"]:7.2f}')
        print(' layers: vp,vs,rho,bottom')

        for layer in result['layers']:
            print(f'{layer["vp"]:7.2f} {layer["vs"]:7.2f} {layer["rho"]:7.2f} {layer["bottom"]:7.2f}')

        print(f' pn,sn,rho-mantle: {result["pn"]:7.2f} {result["sn"]:7.2f} {result["rho_mantle"]:7.2f}')

# 示例用法
if __name__ == "__main__":
    crust_data = CrustData()
    results = crust_data.one_points_query(lat=30, lon=120)
    text_results = crust_data.one_point_query_text(lat=30, lon=120)
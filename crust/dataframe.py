import numpy as np

class CrustData:
    def __init__(self):
        self.np_ = 9
        self.nlo = 360
        self.nla = 180
        self.vp = np.zeros((self.np_, self.nla, self.nlo))
        self.vs = np.zeros((self.np_, self.nla, self.nlo))
        self.rho = np.zeros((self.np_, self.nla, self.nlo))
        self.bnd = np.zeros((self.np_, self.nla, self.nlo))
        self.read_data()

    def read_data(self):
        print(' .... reading all maps ... ')
        with open('crust1.vp', 'r') as f1, \
             open('crust1.vs', 'r') as f2, \
             open('crust1.rho', 'r') as f3, \
             open('crust1.bnds', 'r') as f4:
            for j in range(self.nla):
                for i in range(self.nlo):
                    self.vp[:, j, i] = list(map(float, f1.readline().split()))
                    self.vs[:, j, i] = list(map(float, f2.readline().split()))
                    self.rho[:, j, i] = list(map(float, f3.readline().split()))
                    self.bnd[:, j, i] = list(map(float, f4.readline().split()))

    def get_data_at_location(self, lat, lon):
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

    def interactive_query(self, lat, lon):
        result = self.get_data_at_location(lat, lon)
        print(f'ilat,ilon,crustal type: {result["ilat"]:4d}, {result["ilon"]:4d}')
        print(f'topography: {result["topography"]:7.2f}')
        print(' layers: vp,vs,rho,bottom')

        for layer in result['layers']:
            print(f'{layer["vp"]:7.2f} {layer["vs"]:7.2f} {layer["rho"]:7.2f} {layer["bottom"]:7.2f}')

        print(f' pn,sn,rho-mantle: {result["pn"]:7.2f} {result["sn"]:7.2f} {result["rho_mantle"]:7.2f}')

# 示例用法
if __name__ == "__main__":
    crust_data = CrustData()
    results = crust_data.get_data_at_location(lat=30, lon=120)
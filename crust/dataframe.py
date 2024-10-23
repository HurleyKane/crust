import os
import numpy as np
from crust.config import get_rootPath

vp = os.path.join(get_rootPath(), "source",  'crust1.vp')
vs = os.path.join(get_rootPath(), "source",  'crust1.vs')
rho = os.path.join(get_rootPath(),"source",  'crust1.rho')
bnd = os.path.join(get_rootPath(),"source",  'crust1.bnds')

class CrustResults(dict):
    def __init__(self, seq=None, **kwargs):
        super().__init__(seq, **kwargs)

    def __str__(self):
        string = f'ilat,ilon,crustal type: {self["ilat"]:4d}, {self["ilon"]:4d}\n'
        string += f'topography: {self["topography"]:7.2f}\n'
        string += f'    layers:{" "*9}  vp      vs     rho     bottom     mu     lambda     E       nu\n'
        string += f'{" "*13}        km/s    km/s   g/cm3     km        GPa      GPa     GPa\n'


        layers = [
            '           water',
            '             ice',
            ' upper sediments',
            'middle sediments',
            ' lower sediments',
            ' upper sediments',
            '    middle crust',
            '     lower crust'
        ]

        for index, layer in enumerate(self["layers"]):
            string += f'{layers[index]}  {layer["vp"]:7.2f} {layer["vs"]:7.2f} {layer["rho"]:7.2f} {layer["bottom"]:8.2f}'
            string += f'   {layer["mu"]:7.3f}  {layer["lambda_para"]:7.3f} {layer["E"]:7.3f}  {layer["nu"]:7.3f}\n'
        string += f'pn,sn,rho-mantle {self["pn"]:8.2f} {self["sn"]:7.2f} {self["rho_mantle"]:7.2f}'
        string += f'{self["mu"]:19.3f}  {self["lambda_para"]:7.3f} {self["E"]:7.3f}  {self["nu"]:7.3f}\n'
        return string

class CrustData:
    def __init__(self):
        self.read_data()

    def read_data(self):
        self.np_ = 9
        self.nlo = 360
        self.nla = 180
        self.vp = np.zeros(( self.np_,  self.nla, self.nlo))
        self.vs = np.zeros(( self.np_,  self.nla, self.nlo))
        self.rho = np.zeros((self.np_,  self.nla, self.nlo))
        self.bnd = np.zeros((self.np_,  self.nla, self.nlo))
        with open(vp, 'r') as f1, \
             open(vs, 'r') as f2, \
             open(rho, 'r') as f3, \
             open(bnd, 'r') as f4:
            for j in range(self.nla):
                for i in range(self.nlo):
                    self.vp[:, j, i] = list(map(float, f1.readline().split()))
                    self.vs[:, j, i] = list(map(float, f2.readline().split()))
                    self.rho[:, j, i] = list(map(float, f3.readline().split()))
                    self.bnd[:, j, i] = list(map(float, f4.readline().split()))

    def __getitem__(self, key):
        lat, lon = key
        return self.one_points_query(lat, lon)

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
            rho = self.rho[i-1, ilat-1, ilon-1] * 1e3 # S1 units kg/m3
            vp =  self.vp[i - 1, ilat - 1, ilon - 1] * 1e3 # S1 units m/s
            vs =  self.vs[i - 1, ilat - 1, ilon - 1] * 1e3 # S1 units m/s
            mu = rho * vs**2 # S1 units Pa
            lambda_para = rho*(vp**2-2*vs**2) # S1 units Pa
            if (lambda_para + mu) == 0:
                E = 0
                nu = 0
            else:
                E = (mu * (3*lambda_para+2*mu)) / (lambda_para + mu)
                nu = lambda_para / (2*(lambda_para + mu))
            result['layers'].append({
                'vp': self.vp[i - 1, ilat - 1, ilon - 1],
                'vs': self.vs[i - 1, ilat - 1, ilon - 1],
                'rho': self.rho[i - 1, ilat - 1, ilon - 1],
                'bottom': self.bnd[i, ilat - 1, ilon - 1],
                'mu': mu / 1e9, # 1 Gpa = 1e9 pa
                'lambda_para': lambda_para / 1e9,
                'E': E / 1e9,
                'nu': nu
            })

        rho = self.rho[ - 1, ilat - 1, ilon - 1] * 1e3  # S1 units kg/m3
        vp = self.vp[ - 1, ilat - 1, ilon - 1] * 1e3  # S1 units m/s
        vs = self.vs[ - 1, ilat - 1, ilon - 1] * 1e3  # S1 units m/s
        mu = rho * vs ** 2  # S1 units Pa
        lambda_para = rho * (vp ** 2 - 2 * vs ** 2)  # S1 units Pa
        if (lambda_para + mu) == 0:
            E = 0
            nu = 0
        else:
            E = (mu * (3 * lambda_para + 2 * mu)) / (lambda_para + mu)
            nu = lambda_para / (2 * (lambda_para + mu))
        result['pn'] = self.vp[8, ilat - 1, ilon - 1]
        result['sn'] = self.vs[8, ilat - 1, ilon - 1]
        result['rho_mantle'] = self.rho[8, ilat - 1, ilon - 1]
        result['mu'] = mu / 1e9
        result['lambda_para'] = lambda_para / 1e9
        result['E'] = E / 1e9
        result['nu'] = nu
        return CrustResults(result)


crust_data = CrustData()
print(crust_data[1.5, -40.5])
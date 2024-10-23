# 对crust模型结果的调用

## install
```bash
pip install git@github.com:HurleyKane/crust.git
```
示例:
```python
from crust import crust_data

lat, lon = 32, 100
crust_data[lat, lon]

print(crust_data)
print(dict(crust_data))
```

crust输出结果：
```bash
ilat,ilon,crustal type:   59,  281
topography:    4.12
    layers:           vp      vs     rho     bottom     mu     lambda     E       nu
                     km/s    km/s   g/cm3     km        GPa      GPa     GPa
           water     1.50    0.00    1.02     4.12     0.000    2.295   0.000    0.500
             ice     3.81    1.94    0.92     4.12     3.463    6.430   9.176    0.325
 upper sediments     2.50    1.07    2.11     4.12     2.416    8.356   6.705    0.388
middle sediments     0.00    0.00    0.00     4.12     0.000    0.000   0.000    0.000
 lower sediments     0.00    0.00    0.00     4.12     0.000    0.000   0.000    0.000
     upper crust     6.00    3.52    2.72   -27.49    33.702   30.516  83.419    0.238
    middle crust     6.30    3.68    2.79   -42.67    37.783   35.169  93.781    0.241
     lower crust     6.60    3.82    2.85   -59.10    41.588   40.969 103.815    0.248
pn,sn,rho-mantle     7.98    4.44    3.29             64.858   79.793 165.493    0.276
```

dict(crust_data)输出结果：
```bash
{'E': 165.49266161238026,
 'ilat': 59,
 'ilon': 281,
 'lambda_para': 79.793028,
 'layers': [{'E': 0.0,
             'bottom': 4.12,
             'lambda_para': 2.295,
             'mu': 0.0,
             'nu': 0.5,
             'rho': 1.02,
             'vp': 1.5,
             'vs': 0.0},
            {'E': 9.17558434566845,
             'bottom': 4.12,
             'lambda_para': 6.429788,
             'mu': 3.462512,
             'nu': 0.32498953731690305,
             'rho': 0.92,
             'vp': 3.81,
             'vs': 1.94},
            {'E': 6.705449046169518,
             'bottom': 4.12,
             'lambda_para': 8.356022,
             'mu': 2.415739,
             'nu': 0.38786703492585844,
             'rho': 2.11,
             'vp': 2.5,
             'vs': 1.07},
            {'E': 0.0,
             'bottom': 4.12,
             'lambda_para': 0.0,
             'mu': 0.0,
             'nu': 0,
             'rho': 0.0,
             'vp': 0.0,
             'vs': 0.0},
            {'E': 0.0,
             'bottom': 4.12,
             'lambda_para': 0.0,
             'mu': 0.0,
             'nu': 0,
             'rho': 0.0,
             'vp': 0.0,
             'vs': 0.0},
            {'E': 83.41879623963133,
             'bottom': -27.49,
             'lambda_para': 30.516224,
             'mu': 33.701888,
             'nu': 0.2375982651124966,
             'rho': 2.72,
             'vp': 6.0,
             'vs': 3.52},
            {'E': 93.78111274910125,
             'bottom': -42.67,
             'lambda_para': 35.168508,
             'mu': 37.783296,
             'nu': 0.24103933056953603,
             'rho': 2.79,
             'vp': 6.3,
             'vs': 3.68},
            {'E': 103.81493464201384,
             'bottom': -59.1,
             'lambda_para': 40.96932,
             'mu': 41.58834,
             'nu': 0.24812549192891367,
             'rho': 2.85,
             'vp': 6.6,
             'vs': 3.82}],
 'mu': 64.857744,
 'nu': 0.2758126586424302,
 'pn': 7.98,
 'rho_mantle': 3.29,
 'sn': 4.44,
 'topography': 4.12}
```
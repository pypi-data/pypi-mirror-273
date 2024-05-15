from setuptools import setup


setup(
    name='xbx-Z1',
    version='0.1.0',# 版本号
    description='xbx-Z1',
    author='xbx-Z1',
   
   
    
    install_requires=[  # 用到的库，有需要的往下加
        'numpy==1.24.3',
        'pandas==1.5.3',
        'joblib==1.2.0',
        'ccxt==2.2.79',
        
        'lxml==4.9.2',
        
        'tabulate==0.8.10',
        
        'matplotlib==3.7.1',
        
        'tqdm==4.65.0',
        
        'plotly==5.9.0',
        'loguru==0.6.0',
        'aiofiles==22.1.0',
        'aiohttp==3.8.3',
        'numba==0.57.0',
        'python-dateutil==2.8.2'
    ],
)

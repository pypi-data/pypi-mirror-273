from setuptools import setup, find_packages  
  
setup(  
    name='pytech-zp',  
    version='0.0.1',  
    author='Peng Zhao',
    license='MIT',
    description='Python function package of technical indicators and patterns implemented by C++',
    packages=find_packages(),
    package_data={'pytech-zp': ['pytech.cp39-win_amd64.pyd']},
    # 其他必要信息，如 author, description, license 等  
)
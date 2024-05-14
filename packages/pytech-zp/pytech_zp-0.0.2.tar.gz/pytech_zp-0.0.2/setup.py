from setuptools import setup, find_packages
  
setup(  
    name='pytech-zp',  
    version='0.0.2',  
    author='Peng Zhao',
    description='Python function package of technical indicators and patterns implemented by C++',
    packages=find_packages(),
    package_data={'pytech': ['*.pyd']},
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license=open('LICENSE').read(),
    # 其他必要信息，如 author, description, license 等  
)
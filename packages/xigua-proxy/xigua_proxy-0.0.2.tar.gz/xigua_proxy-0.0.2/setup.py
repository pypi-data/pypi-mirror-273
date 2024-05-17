from distutils.core import setup
# import setuptools

packages = ['xigua_proxy']
setup(name='xigua_proxy',
      version='0.0.2',
      author='xigua, 获取一个随机代理ip',
      packages=packages,
      package_dir={'requests': 'requests'}, )

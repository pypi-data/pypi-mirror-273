from distutils.core import setup
# import setuptools

packages = ['bdup']
setup(name='bdup',
      version='0.0.1',
      author='xigua, 百度云上传下载, 需要调用 bypy 库',
      packages=packages,
      package_dir={'requests': 'requests'}, )

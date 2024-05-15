from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='rltexe',
  version='0.0.1',
  description='rlt experiments',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='BigSmoke',
  author_email='gurusmart555@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='wteam', 
  packages=find_packages(),
  include_package_data= True,
  install_requires=[''] 
)
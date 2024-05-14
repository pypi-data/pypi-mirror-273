from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ishandaiexperiments',
  version='0.0.3',
  description='dai experiments',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='S Ishan',
  author_email='is9678@srmist.edu.in',
  license='MIT', 
  classifiers=classifiers,
  keywords='dai', 
  packages=find_packages('exp'),
  include_package_data= True,
  install_requires=[''] 
)
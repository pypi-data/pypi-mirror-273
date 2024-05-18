from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='JsonsTest',
  version='0.0.3',
  author='sonin',
  author_email='fediasonin@gmail.com',
  description='This is the simplest module for quick work with json files.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  python_requires='>=3.6'
)
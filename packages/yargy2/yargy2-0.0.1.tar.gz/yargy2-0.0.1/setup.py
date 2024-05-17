from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='yargy2',
  version='0.0.1',
  author='Karina',
  author_email='minyailo.karina@gmail.com',
  description='This is a yargy library, but now it interacts well with pymorphy3.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/mininakar/yargy2',
  packages=find_packages(),
  install_requires=['pymorphy3>=2.0.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files yargy pymorphy3 ',
  project_urls={
    'GitHub': 'https://github.com/mininakar'
  },
  python_requires='>=3.6'
)
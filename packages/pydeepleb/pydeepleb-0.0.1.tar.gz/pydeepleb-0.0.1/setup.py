from setuptools import setup, find_packages




setup(
  name='pydeepleb',
  version='0.0.1',
  author='garik-g',
  author_email='example@gmail.com',
  description='This is the simplest module for quick work with files.',
  long_description='This is the simplest module for quick work with files.',
  long_description_content_type='text/markdown',
  url='https://www.youtube.com/',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://www.youtube.com/'
  },
  python_requires='>=3.6'
)
from setuptools import setup

from py_sa._version import __version__

setup(name='py_sa',
      version=__version__,
      description='Interact with aegea and s3 through python',
      author='Matt Olm',
      author_email='mattolm@stanford.edu',
      license='MIT',
      packages=['py_sa'],
      install_requires=[
          'pandas',
          'boto3'
      ],
      zip_safe=False)
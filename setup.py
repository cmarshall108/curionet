try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = '''
An asynchronous high-level networking framework built on top of the Curio library.
'''

setup(name='Curionet',
      description='Curionet, curio based framework.',
      long_description=long_description,
      license='Apache 2.0',
      version='1.0.0',
      author='Caleb Marshall',
      author_email='anythingtechpro@gmail.com',
      maintainer='Caleb Marshall',
      maintainer_email='anythingtechpro@gmail.com',
      url='https://github.com/AnythingTechPro/Curionet',
      packages=['curionet'],
      classifiers=[
          'Programming Language :: Python :: 3',
      ])

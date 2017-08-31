from setuptools import setup

setup(name='smuploader',
      version='0.3',
      description='A SmugMug uploader and downloader. Uses SmugMug API v2.0',
      url='http://github.com/marekrei/smuploader',
      author='Marek Rei, Erik Selberg',
      author_email='marek@marekrei.com, erik@selberg.org',
      license='MIT',
      packages=['smuploader'],
      scripts=['bin/smuploader', 'bin/smdownloader', 'bin/smregister', 'bin/smregtest'],
      zip_safe=False)

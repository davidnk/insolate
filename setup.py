from distutils.core import setup

setup(
    name='insolater',
    version='0.0.1',
    packages=['insolater'],
    author='David Karesh',
    author_email='davidnk@gmail.com',
    url='github.com/davidnk/insolater',
    license='LICENSE.txt',
    description='Tool to easily switch between original and modified versions of a directory.',
    entry_points={'console_scripts': ['inso = insolater.run:main']},
    )

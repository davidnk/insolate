try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup

packages = ['insolater'],
requires = []

with open('README.md') as f:
    readme = f.read()
with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='insolater',
    version='0.0.1',
    description='Tool to easily switch between original and modified versions of a directory.',
    long_description=readme,
    author='David Karesh',
    author_email='davidnk@gmail.com',
    url='github.com/davidnk/insolater',
    packages=['insolater'],
    install_requires=[],
    license=license,
    entry_points={'console_scripts': ['inso = insolater.run:main']},
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)

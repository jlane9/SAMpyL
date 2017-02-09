"""SAMpyL setup.py
"""

from setuptools import setup, find_packages
from sampyl import __author__, __email__, __license__, __version__

setup(
    name='sampyl',
    version=__version__,
    packages=find_packages(),
    description='A wrapper for Selenium. This library uses custom data attributes to accelerate '
                'testing through the Selenium framework',
    author=__author__,
    author_email=__email__,
    url='https://github.com/jlane9/SAMpyL',
    download_url='https://github.com/jlane9/SAMpyL/tarball/%s' % __version__,
    keywords='testing selenium qa web automation',
    install_requires=['lxml', 'cssselect', 'PyYAML'],
    license=__license__,
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: MIT License',
                 'Topic :: Software Development :: Quality Assurance',
                 'Topic :: Software Development :: Testing'])

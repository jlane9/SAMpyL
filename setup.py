from setuptools import setup, find_packages


setup(
    name='sampyl',
    version='0.0.5',
    packages=find_packages(),
    description='A wrapper for Selenium. This library uses custom data attributes to accelerate testing '
    'through the Selenium framework',
    author='John Lane',
    author_email='jlane@fanthreesixty.com',
    url='https://github.com/jlane9/SAMpyL',
    download_url='https://github.com/jlane9/SAMpyL',
    keywords='testing selenium qa web automation',
    install_requires=[],
    license='MIT',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: MIT License',
                 'Topic :: Software Development :: Quality Assurance',
                 'Topic :: Software Development :: Testing'])

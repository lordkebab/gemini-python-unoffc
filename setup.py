from setuptools import setup, find_packages

import gemini

setup(
    name='gemini-python-unoffc',
    version=gemini.__version__,
    packages=find_packages(),
    install_requires=['requests>=2.13.0'],
    author='Matt Selph',
    author_email='mattselph@outlook.com',
    description='An Unofficial Python library for the Gemini Exchange REST API.',
    license='MIT',
    keywords='bitcoin ethereum api gemini',
    url='https://github.com/mattselph/gemini-python-unoffc',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

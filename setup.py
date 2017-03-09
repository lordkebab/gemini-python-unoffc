from distutils.core import setup

import gemini

setup(
    name='gemini-python',
    version=gemini.__version__,
    download_url='https://github.com/mattselph/gemini-python-unoffc/tarball/%s' % (gemini.__version__),
    description='Unofficial Python library for the Gemini Exchange REST API.',
    author='Matt Selph',
    author_email='mattselph@outlook.com',
    license='MIT License',
    url='https://github.com/mattselph/gemini-python-unoffc',
    packages=['gemini'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords = ['api', 'bitcoin', 'ethereum', 'gemini']
)

from setuptools import setup

setup(
    name='pyhistogram',
    version='0.1',
    description="Simple histogram classes, with minimal dependencies",
    author='Christian Bourjau',
    author_email='c.bourjau@gmx.net',
    packages=['pyhistogram', 'pyhistogram.tests'],
    license=open('LICENSE.txt').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/chrisboo/pyhistogram',
    download_url='https://github.com/chrisboo/pyhistogram/tarball/0.1',
    keywords=['histogram', 'statistics'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # install_requires=['numpy', 'matplotlib'],
    extras_require={
        'plotting':  ["matplotlib"]
    },
    test_suite='pyhistogram.tests',
)

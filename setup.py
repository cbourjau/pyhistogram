from setuptools import setup

setup(
    name='pyhistogram',
    version='0.1',
    description="Convinient and intuitive histograms with minimal dependencies",
    author='Christian Bourjau',
    author_email='c.bourjau@gmx.net',
    packages=['pyhistogram', 'pyhistogram.tests'],
    long_description=open('README.rst').read(),
    url='https://github.com/chrisboo/pyhistogram',
    download_url='https://github.com/chrisboo/pyhistogram/tarball/0.1',
    keywords=['histogram', 'statistics'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # install_requires=['numpy', 'matplotlib'],
    extras_require={
        'plotting':  ["matplotlib"]
    },
    test_suite='pyhistogram.tests',
)

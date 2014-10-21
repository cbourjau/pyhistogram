import os
from pkg_resources import resource_filename

__all__ = [
    'get_filepath',
    'get_file',
]


def get_filepath(name='hamlet.txt'):
    return resource_filename('pyhistogram', os.path.join('testdata', name))


def get_file(name='hamlet.txt'):
    filepath = get_filepath(name)
    if not os.path.isfile(filepath):
        raise ValueError(
            "pyhistogram test data file {0} does not exist".format(filepath))
    return open(filepath, 'r')

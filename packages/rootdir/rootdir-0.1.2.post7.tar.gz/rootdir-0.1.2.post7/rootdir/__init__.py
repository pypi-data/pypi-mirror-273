import os
import sys

class FailToFindRootException(Exception):
    pass


def root_dir(__file__):
    current_directory = os.path.dirname(__file__)

    while True:
        if os.path.exists(os.path.join(current_directory, '__root__.py')):
            return current_directory

        if current_directory == "/" or current_directory == os.path.dirname(current_directory):
            raise FailToFindRootException("There is no _root__.py, " + current_directory)

        current_directory = os.path.dirname(current_directory)


def root_dependency(__file__):
    root_directory = root_dir(__file__)
    sys.path.append(root_directory)
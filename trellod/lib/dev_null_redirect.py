#!/usr/bin/env python

""" Contains DevNullRedirect """

import os


class DevNullRedirect:
    """ Context manager temporarily sends stdout/stderr to dev/null to prevent output """

    def __init__(self):
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        self.old_stdout = os.dup(1)
        self.old_stderr = os.dup(2)
        os.close(1)
        os.close(2)
        os.open(os.devnull, os.O_RDWR)

    def __exit__(self, exc_type, exc_value, traceback):
        os.dup2(self.old_stdout, 1)
        os.dup2(self.old_stderr, 2)


def demo():
    """ DevNullRedirect() example """
    print("Now you see me...")
    with DevNullRedirect():
        print("Now you don't!")
    print("Don't forget to tip your server")


if __name__ == "__main__":
    demo()

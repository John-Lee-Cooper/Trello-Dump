#!/usr/bin/env python

""" Command Line Interface functions """

import sys
from enum import IntEnum
from typing import Any, Callable

import click
import typer
from str_enum import StrEnum


def bell():
    sys.stdout.write("\a")
    sys.stdout.flush()


def run(function: Callable[..., Any]) -> Any:
    """ TODO """
    app = typer.Typer(add_completion=False)
    command = app.command()
    command(function)
    app()


class Color(StrEnum):
    """ TODO """

    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"


class Key(IntEnum):
    """ TODO """

    # vi
    BACKSPACE_2 = 8
    ENTER_2 = 10
    # TAB_2 = 9
    # ESCAPE_2 = 27

    # bash
    BACKSPACE = 127
    ENTER = 13
    CTRL_C = 3
    ESC = 27  # 10
    TAB = 9

    U_ARROW = 97  # (72, 117, 65)
    D_ARROW = 98  # (80, 100, 66)
    R_ARROW = 99  # (77, 114, 67)
    L_ARROW = 100  # (75, 108, 68)


class Style:
    """ TODO """

    def __init__(
        self,
        fg=None,
        bg=None,
        bold=None,
        dim=None,
        underline=None,
        blink=None,
        reverse=None,
        reset=True,
    ):
        self.style = dict(
            fg=fg,
            bg=bg,
            bold=bold,
            dim=dim,
            underline=underline,
            blink=blink,
            reverse=reverse,
            reset=reset,
        )

    def __call__(self, text):
        return click.style(text, **self.style)

    def echo(self, text="", **kw):
        """ TODO """
        click.echo(self(text), **kw)

    def prompt(self, text="", **kw):
        """ TODO """
        return click.prompt(self(text), **kw)

    def confirm(self, text="", **kw):
        """ TODO """
        return click.confirm(self(text), **kw)

    def pause(self, text="", **kw):
        """ TODO """
        return click.pause(self(text), **kw)


if __name__ == "__main__":
    bell()

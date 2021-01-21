#!/usr/bin/env python

""" TODO """

from typing import List, Optional

from cli import Style
from typer import echo


def select(
    options: list, title: str = "", prompt: str = "Select", style: Style = None
) -> Optional[int]:
    """ TODO """

    if not options:
        return None

    style = style or Style()

    if title:
        echo(title)

    for index, string in enumerate(options):
        echo(style(f"{index+1:3}: ") + str(string))

    while True:
        selected = style.prompt(prompt, type=int)

        if selected == 0:
            return None
        if 0 < selected <= len(options):
            return selected - 1
        echo(f"Error: {selected} is out of range")


def demo():
    """ Demonstrate select """

    options = (
        "First shalt thou take out the Holy Pin.",
        "Then, shalt thou count to three. No more.  No less."
        "Three shalt be the number thou shalt count, and the number of the counting shall be three.",
        "Four shalt thou not count, nor either count thou two, excepting that thou then proceed to three.",
        "Five is right out.",
        "Once the number three, being the third number, be reached,",
        "then, lobbest thou thy Holy Hand Grenade of Antioch towards thy foe,",
        "who, being naughty in My sight, shall snuff it.",
    )
    index = select(options, style=Style(fg="green"))
    if index is not None:
        print(options[index])


if __name__ == "__main__":
    demo()

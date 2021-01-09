#!/usr/bin/env python

"""
Trello Dump Utility

Build trello export cli
  Write <board_name>.csv with columns:
    <list_name> <card_name> <card_desc> <card_has_todo> <card_has_attach>
  Handle logging into trello and storing keys
"""

import sys
import webbrowser
from pathlib import Path
from urllib import request

import pandas as pd
from trello import TrelloClient

from .authorize import authorize
from .lib.cli import Style
from .lib.cli_select import select
from .lib.config import Config
from .lib.string_util import safe_filename

style = Style(fg="green")


def login(config) -> TrelloClient:
    """
    Login to Trello

    Where token and token_secret come from the 3-legged OAuth process
    To use without 3-legged OAuth, use only api_key and api_secret on client.
    """
    return TrelloClient(
        api_key=config.api_key,
        api_secret=config.api_secret,
        token=config.oauth_token,
        token_secret=config.oauth_token_secret,
    )


def select_board(client, board_name=None):
    """ get client's board named board_name """

    boards = [board for board in client.list_boards() if not board.closed]

    if board_name:
        for board in boards:
            if board.name == board_name:
                return board

    board_names = [board.name for board in boards]
    while True:
        index = select(board_names, prompt="Select Board: ", style=style)
        if index is None:
            sys.exit(0)
        return boards[index]


def select_lists(board) -> list:
    """ TODO """
    lists = board.open_lists()

    list_names = [f"{list_.name} ({list_.cardsCnt()})" for list_ in lists]
    title = f"\nBoard:  {board.name}"
    while True:
        index = select(list_names, title=title, prompt="Select List: ", style=style)
        if index is None:
            return lists
        return [lists[index]]


def pad_dict_list(dict_list, padding) -> None:
    """ make lists in dict_list have the same length by appending padding """

    max_length = max(len(list_) for list_ in dict_list.values())
    for list_ in dict_list.values():
        list_ += [padding] * (max_length - len(list_))


def column_width(df, field_name, max_width=None) -> int:
    """ TODO """

    series = df[field_name]
    width = max(
        len(str(series.name)),  # len of column name/header
        series.astype(str).map(len).max(),  # len of largest item
    )
    return width if max_width is None else min(width, max_width)


def df_to_excel(df, excel, sheet_name, max_width=60):
    """ TODO """

    # num_rows = len(df.index)
    num_cols = len(df.columns)

    cell_format = excel.book.add_format(
        dict(
            text_wrap=True,
            align="top",
            # bg_color="#FFFFDD",
            border=1,
            border_color="#808080",
        )
    )

    df.to_excel(
        excel,
        sheet_name=sheet_name,
        index=False,
    )
    worksheet = excel.sheets[sheet_name]

    # Hide unused cells
    worksheet.set_default_row(height=None, hide_unused_rows=True)
    worksheet.set_column(num_cols, 16383, options=dict(hidden=True))

    options = dict(hidden=False)
    for col, field_name in enumerate(df):  # loop through all columns
        width = column_width(df, field_name, max_width)
        worksheet.set_column(col, col, width, cell_format, options)


def dump_trello(filename: str, lists: list) -> None:
    """ TODO """

    excel = pd.ExcelWriter(
        filename, engine="xlsxwriter"
    )  # pylint: disable=abstract-class-instantiated

    sheet_name = "Board"
    data = {
        list_.name.strip(): [card.name.strip() for card in list_.list_cards()]
        for list_ in lists
    }
    pad_dict_list(data, "")
    df = pd.DataFrame(data)
    df_to_excel(df, excel, sheet_name)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    # Convert the dataframe to an XlsxWriter Excel object.
    # Close the Pandas Excel writer and output the Excel file.
    for list_ in lists:
        sheet_name = f"List {list_.name}"

        cards, desc, items, att = [], [], [], []
        for card in list_.list_cards():
            cards.append(card.name.strip())
            desc.append(card.description.strip())
            items.append(
                "\n".join(
                    [
                        "\n".join([item["name"].strip() for item in checklist.items])
                        for checklist in card.checklists
                    ]
                )
            )
            att.append(
                "\n".join([attachment.url for attachment in card.get_attachments()])
            )

        df = pd.DataFrame(
            dict(Card=cards, Description=desc, Todo=items, Attachments=att)
        )
        df_to_excel(df, excel, sheet_name)

    excel.save()


def download_images(card) -> None:
    """ TODO """
    for attachment in card.get_attachments():
        mime_type = attachment.mime_type.split("/")
        if mime_type[0] != "image":
            continue
        ext = mime_type[1]
        if ext == "jpeg":
            ext = "jpg"
        filename = safe_filename(f"{card.name}.{ext}")
        request.urlretrieve(attachment.url, filename)


def download_images_in_lists(lists) -> None:
    """ TODO """
    for list_ in lists:
        for card in list_.list_cards():
            download_images(card)


def main() -> None:
    """ TODO """

    config = Config(
        basename="trellod",
        api_key=None,
        api_secret=None,
        oauth_token=None,
        oauth_token_secret=None,
    )
    if config.api_key is None:
        config.set(**authorize())

    client = login(config)

    board_name = None
    board = select_board(client, board_name)
    # lists = select_lists(board)
    lists = board.open_lists()

    filename = f"Trello {board.name.strip()}.xlsx"
    dump_trello(filename, lists)
    # download_images_in_lists(lists)

    webbrowser.open(f"file://{Path(filename).resolve()}")


if __name__ == "__main__":
    main()

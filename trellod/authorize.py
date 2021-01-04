#!/usr/bin/env python

"""
Walk user through Oauth process for Trello
"""

import sys
import webbrowser
from typing import Dict

from click import clear
from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenRequestDenied

from .lib.dev_null_redirect import DevNullRedirect
from .lib.cli import Style


err_style = Style(fg="red")
msg_style = Style(fg="green")


def open_webpage(url: str) -> None:
    """ TODO """

    msg_style.echo(f"\t{url}")
    with DevNullRedirect():
        webbrowser.open(url, new=0)


def authorize(app_name="this app") -> Dict[str, str]:
    """
    Obtain Trello API credentials and put them into your config file.
    The configuration file is put in an appropriate place for your operating system.
    """

    login_url = "https://trello.com"
    user_api_key_url = "https://trello.com/app-key"
    authorize_url = "https://trello.com/1/OAuthAuthorizeToken"
    request_token_url = "https://trello.com/1/OAuthGetRequestToken"
    access_token_url = "https://trello.com/1/OAuthGetAccessToken"

    clear()
    msg_style.echo(
        f"You have not authorized Trello to use {app_name}.  To get an auth token, log into Trello:"
    )
    open_webpage(login_url)
    while not msg_style.confirm("Are you logged in?", default=False):
        pass
    msg_style.echo()

    msg_style.echo("Next, browser to the following URL:")
    open_webpage(user_api_key_url)
    api_key = msg_style.prompt(
        "Copy the 'Key' in a text box, and paste for here"
    ).strip()  # confirmation_prompt=True)
    msg_style.echo()

    msg_style.echo("Next, scroll to the bottom of the page.")
    api_secret = msg_style.prompt(
        "Copy the 'Secret:' from the text box, and paste here"
    ).strip()
    msg_style.echo()

    # The following code is derived from trello.util.create_oauth_token from py-trello,
    # rewritten because it did not support opening the auth URLs using webbrowser.open and click.

    # Step 1: Get a request token.
    # This is a temporary token that is used for
    # having the user authorize an access token and to sign the request to obtain said access token.
    session = OAuth1Session(client_key=api_key, client_secret=api_secret)
    try:
        response = session.fetch_request_token(request_token_url)
    except TokenRequestDenied:
        err_style.echo(f"Invalid API key/secret provided: {api_key} / {api_secret}")
        sys.exit(1)
    resource_owner_key = response.get("oauth_token")
    resource_owner_secret = response.get("oauth_token_secret")

    # Step 2: Redirect to the provider.
    # Since this is a CLI script we do not redirect.
    # In a web application you would redirect the user to the URL below.
    user_confirmation_url = f"{authorize_url}?" + "&".join(
        (
            f"oauth_token={resource_owner_key}",
            "scope=read,write",
            "expiration=never",
            "name=trellod.py ",
        )
    )
    msg_style.echo(
        f"Browse to the following URL to authorize {app_name} to access your Trello account:"
    )
    open_webpage(user_confirmation_url)

    # After the user has granted access to you, the consumer,
    # the provider will redirect you to whatever URL you have told them to redirect to.
    # You can usually define this in the oauth_callback argument as well.

    while not msg_style.confirm(f"Have you authorized {app_name}?", default=False):
        pass
    oauth_verifier = msg_style.prompt(
        "Copy the verification code in the text box, and paste for here"
    ).strip()
    msg_style.echo()

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved.
    # You use the request token to sign this request.
    # After this is done you throw away the request token and use the access token returned.
    # You should store this access token somewhere safe, like a database, for future use.
    session = OAuth1Session(
        client_key=api_key,
        client_secret=api_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=oauth_verifier,
    )
    access_token = session.fetch_access_token(access_token_url)

    config = dict(
        api_key=api_key,
        api_secret=api_secret,
        oauth_token=access_token["oauth_token"],
        oauth_token_secret=access_token["oauth_token_secret"],
    )
    return config

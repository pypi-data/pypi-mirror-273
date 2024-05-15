from urllib.parse import unquote
from click import command, echo, argument

@command()
@argument("url_string")
def urldecode(url_string):
    utf_string = unquote(url_string)
    echo(f"{utf_string}")

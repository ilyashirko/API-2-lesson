# Clipping links with bit.ly
Generates short links bit.ly and counts the number of clicks on such links

## How to install
### You will need a token to work.
You can get it here:
>https://app.bitly.com/settings/api/

Register, enter a password and click "Generate token"
The token looks something like this: 
>"3ig534hv53uv5ih4gjh34gb5jh3bjhb345b3j5b"

It must be placed in the ".env" file after the "=" sign
It should turn out like this:
>BITLINK_TOKEN=3ig534hv53uv5ih4gjh34gb5jh3bjhb345b3j5b

### Installing dependencies.
You will need python3 and pip (pip3).
> pip3 install -r requirement.txt

## How to start
instead of LINK, enter a link in the format "http://www.google.com"
>$python3 main.py LINK


# Description of main.py functions
## is_bitlink
Checks if the link is shortened.
If it is a bitlink, returns True, otherwise False

## count_click
If the link you entered is abbreviated:
 - requests the number of transitions on it;
 - displays on the screen in case of a successful server response.
 - displays an error if there is no response.

## shorten_link
Requests a shortened link from the server for the entered link.
The link must be specified in full, with the protocol, otherwise an error will be displayed.
Displays the received link

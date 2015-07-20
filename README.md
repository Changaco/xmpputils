# A collection of XMPP utils

`echobot.py` is a bot that just echoes back whatever message you send to it. Useful for testing purposes.

`sendxmpp.py` is the XMPP equivalent of sendmail. It is an alternative to the old sendxmpp written in Perl.

Dependencies:
 
- python 3
- dnspython
- sleekxmpp

To install them on Ubuntu:

    sudo apt-get install python3 python3-pip
    sudo pip install dnspython sleekxmpp

Installation: just put the scripts wherever you want.

Configuration: `cp CONFIG.example ~/.xmpputils` and edit `~/.xmpputils` with your XMPP credentials

Usage examples:

- `echo "This is a test" | sendxmpp.py user@host`
- `sendxmpp.py user@host <README.md`

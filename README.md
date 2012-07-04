steamsale.py
============

A Python script for retrieving your Steam wishlist.

It can be combined with a crontab and send notifications if there are any items
in your wishlist that are currently on sale.

Usage
=====
    $ python steamsale.py
    usage: steamsale.py [OPTIONS] steam_id
     -h, --help         Display usage
     -s, --sale         Show only items that are on sale
     -c, --colors       Use colors in output
     -d, --dump         Dump dictionary

You'll need your Steam ID from the wishlist URL:

    http://steamcommunity.com/profiles/[this_one]/wishlist

Dependencies
============

* requests - http://docs.python-requests.org
* BeautifulSoup - http://www.crummy.com/software/BeautifulSoup
* termcolor - http://pypi.python.org/pypi/termcolor
* PyYAML - http://pyyaml.org/wiki/PyYAML

Create and initialize virtualenv:

    virtualenv --distribute venv
    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

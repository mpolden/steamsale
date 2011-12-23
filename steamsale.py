#!/usr/bin/env python

""" A script that parses your Steam wishlist and finds discounts """

import sys
import requests
from re import sub
from getopt import getopt, GetoptError
from BeautifulSoup import BeautifulSoup
from termcolor import colored

class Wishlist(object):
    """ Class representing a Steam wishlist """
    def __init__(self, steam_id):
        url = 'http://steamcommunity.com/profiles/%s/wishlist' % steam_id
        req = requests.get(url)
        self.soup = BeautifulSoup(req.content,
                convertEntities=BeautifulSoup.HTML_ENTITIES)
        self.tag = None
        self.items = []

    def _find_price(self):
        """ Find default price or None """
        price = self.tag.find(attrs = {'class': 'price'})
        return price.text if price and price.text else None

    def _find_discount_pct(self):
        """ Returns discount percentage or None """
        discount_pct = self.tag.find(attrs = {'class': 'discount_pct'})
        return discount_pct.text if discount_pct else None

    def _find_org_price(self):
        """ Returns original price or None """
        org_price = self.tag.find(attrs = {'class': 'discount_original_price'})
        return org_price.text if org_price else None

    def _find_final_price(self):
        """ Returns discounted final price or None """
        final_price = self.tag.find(attrs = {'class': 'discount_final_price'})
        return final_price.text if final_price else None

    def find_items(self, only_sale=False):
        """ Parse and find wishlist items """
        # Find divs containing wishlist items
        item_tags = self.soup.findAll(attrs = {'class': "wishlistRowItem\t"})
        for item_tag in item_tags:
            self.tag = item_tag.find(attrs = {'class': 'gameListPriceData'})
            title = item_tag.find('h4').text
            default_price = self._find_price()
            discount_pct = self._find_discount_pct()
            original_price = self._find_org_price()
            final_price = self._find_final_price()

            if only_sale and not discount_pct:
                continue
            self.items.append({
                'title': title,
                'discount_pct': discount_pct,
                'original_price': original_price,
                'final_price': default_price or final_price
                })

        return self.items

    def prettify(self, colors):
        """ Create a string representation of items """
        lines = []
        for item in self.items:
            if item['discount_pct']:
                lines.append('%s is on sale for %s, down from %s (%s)' % \
                        (colored(item['title'], attrs=['bold']),
                                colored(item['final_price'], 'green'),
                                colored(item['original_price'], 'red'),
                                colored(item['discount_pct'], 'cyan')))
            elif item['final_price']:
                lines.append('%s is not on sale and costs %s' % \
                        (colored(item['title'], attrs=['bold']),
                                colored(item['final_price'], 'yellow')))
            else:
                lines.append('%s has no price (yet?)' % colored(item['title'],
                        attrs=['bold']))
        out = '\n'.join(lines)
        return out if colors else sub(r'\x1b\[\d+m', '', out) # Hack!

def usage():
    """ Display usage """
    print ('usage: %s [OPTIONS] steam_id'
    '\n -h, --help\t\tDisplay usage'
    '\n -s, --sale\t\tShow only items that are on sale'
    '\n -c, --colors\t\tUse colors in output') % sys.argv[0]
    sys.exit(1)

def main():
    """ Parse argv, find items and print them to stdout """
    try:
        opts, args = getopt(sys.argv[1:], 'hsc', ['help', 'sale',
                'colors'])
    except GetoptError, err:
        print str(err)
        usage()

    if not args:
        usage()

    steam_id = args[0]
    only_sale = False
    colors = False
    print opts
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-s', '--sale'):
            only_sale = True
        elif opt in ('-c', '--colors'):
            colors = True

    wishlist = Wishlist(steam_id)
    wishlist.find_items(only_sale)
    print wishlist.prettify(colors)

if __name__ == '__main__':
    main()

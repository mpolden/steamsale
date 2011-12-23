#!/usr/bin/env python

""" A script that parses your Steam wishlist and finds discounts """

import sys
import requests
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

    def find_items(self):
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

            self.items.append({
                'title': title,
                'discount_pct': discount_pct,
                'original_price': original_price,
                'final_price': default_price or final_price
                })

        return self.items

    def prettify(self):
        """ Create a string representation of items """
        out = []
        for item in self.items:
            if item['discount_pct']:
                out.append('%s is on sale for %s, down from %s (%s)' % \
                        (colored(item['title'], attrs=['bold']),
                                colored(item['final_price'], 'green'),
                                colored(item['original_price'], 'red'),
                                colored(item['discount_pct'], 'cyan')))
            elif item['final_price']:
                out.append('%s is not on sale and costs %s' % \
                        (colored(item['title'], attrs=['bold']), 
                                colored(item['final_price'], 'yellow')))
            else:
                out.append('%s has no price (yet?)' % colored(item['title'], 
                        attrs=['bold']))
        return '\n'.join(out)

def usage():
    """ Display usage """
    print 'usage: %s steam_id' % sys.argv[0]

def main():
    """ Parse argv, find items and print them to stdout """
    if len(sys.argv) != 2:
        usage()
        return
    steam_id = sys.argv[1]
    
    wishlist = Wishlist(steam_id)
    wishlist.find_items()
    print wishlist.prettify()

if __name__ == '__main__':
    main()

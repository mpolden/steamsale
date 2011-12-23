#!/usr/bin/env python

import sys
import requests
from BeautifulSoup import BeautifulSoup

def usage():
    print 'usage: %s steam_id' % sys.argv[0]

def find_items(steam_id):
    wishlist_url = 'http://steamcommunity.com/profiles/%s/wishlist' % steam_id

    r = requests.get(wishlist_url)
    soup = BeautifulSoup(r.content, 
            convertEntities=BeautifulSoup.HTML_ENTITIES)
    items = []

    # Find divs containing wishlist items
    item_tags = soup.findAll(attrs = {'class': "wishlistRowItem\t"})
    for item_tag in item_tags:
        title = item_tag.find('h4').text

        # Find div containing price data
        data_tag = item_tag.find(attrs = {'class': 'gameListPriceData'})

        # Find default price
        p_tag = data_tag.find(attrs = {'class': 'price'})
        default_price = p_tag.text if p_tag and p_tag.text else None
       
        # Find discount percent if any
        dp_tag = data_tag.find(attrs = {'class': 'discount_pct'})
        discount_pct = dp_tag.text if dp_tag else None

        # Original price    
        dop_tag = data_tag.find(attrs = {'class': 'discount_original_price'})
        original_price = dop_tag.text if dop_tag else None

        # Final price
        dfp_tag = data_tag.find(attrs = {'class': 'discount_final_price'})
        discount_price = dfp_tag.text if dfp_tag else None

        items.append({
            'title': title,
            'discount_pct': discount_pct,
            'original_price': original_price,
            'final_price': default_price or discount_price
            })

    return items

def main():

    if len(sys.argv) != 2:
        usage()
        return

    steam_id = sys.argv[1]

    items = find_items(steam_id)
    for item in items:
        print '%s - price: %s' % (item['title'], item['final_price'])

if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup
import re
    
    
"""
Takes a wikipedia url and returns its paragraphs in plaintext and
infoboxes as a single dictionary, where each key-value pair
represents a row in an infobox table. 
"""
def scrape_article(url):
    response = requests.get(url, headers={'User-Agent': 'wikipedia infobox generation'})
    if response.status_code != 200:
        return '', {}
    
    # extract article paragraphs
    soup = BeautifulSoup(response.text, 'html.parser')
    ps = soup.find_all('p')

    # strip whitespace to avoid empty paragraphs
    paragraphs = []
    for p in ps:
        p = p.get_text().strip()
        if len(p) > 0:
            paragraphs.append(p)

    # extract article infoboxes as key-value pairs
    infoboxes = soup.find_all('table', class_='infobox')
    infobox_dict = {}

    for infobox in infoboxes:
        table_rows = infobox.find_all('tr')

        for row in table_rows:
            cells = row.find_all(['th', 'td'])
            if len(cells) == 2:
                key = cells[0].get_text().strip()
                value = format_infobox_value(cells[1])
                key, value = format_infobox_pair(key, value)
                infobox_dict[key] = value

    return paragraphs, infobox_dict


"""
Remove footnotes from infobox keys and values
"""
def format_infobox_pair(key, value):
    pattern = r'\[\d+\]' # matches [digits] at end of string
    key = re.sub(pattern, '', key).lower()
    value = re.sub(pattern, '', value).lower()
    return key, value


""" 
Handle cases where infobox values are html lists, which by default return
concatenated with no spaces. Return the result, where everything is separated
by a single space
"""
def format_infobox_value(cell):
    value_soup = BeautifulSoup(cell.encode_contents(), 'html.parser')
    value = value_soup.get_text(separator=' ').strip()
    value = re.sub(r'\s+', ' ', value) # remove consecutive spaces
    return value

"""================================================================================================
This script accesses each 'Letter to Shareholders' from Berkshire Hathaway's online archive.

12/23/22   Ben Iovino   BuffettLetters
================================================================================================"""

import os
import requests
import PyPDF2
from bs4 import BeautifulSoup


def get_links(url, headers):
    """=============================================================================================
    This function takes a url and gathers all links. It returns a list of the desired links.

    :param url: root url
    :param headers: headers used for requests
    :return: list of links
    ============================================================================================="""

    # Request url and parse html
    page = requests.get(url, headers=headers, timeout=5)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get links to individual letters
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    links = links[1:-1]

    return links


def get_html(url, links, headers):
    """=============================================================================================
    This function takes a url and list of sublinks that lead to html webpages and writes their
    text content to an individual file.

    :param url: root url
    :param links: list of links leading to individual webpages
    :param headers: headers used for requests
    ============================================================================================="""

    # Iterate over each webpage
    for link in links:

        # Get content of webpage, parse with beautiful soup
        content = requests.get(url+link, headers=headers, timeout=5)
        letter = BeautifulSoup(content.text, 'html.parser')

        # Write to file as is
        if not os.path.exists('html_letters'):
            os.mkdir('html_letters')
        with open(f'html_letters/{link}', 'w', encoding='utf8') as file:
            file.write(str(letter))


def main():
    """=============================================================================================
    ============================================================================================="""

    # Set user-agent hearder for requests (UA below sent by personal machine)
    headers = {'User-Agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'}

    # Get all links from url
    url = 'https://www.berkshirehathaway.com/letters/letters.html'
    links = get_links(url, headers)

    # Get letters from html webpages
    url = 'https://www.berkshirehathaway.com/letters/'
    html_letters = links[:21]
    #get_html(url, html_letters, headers)

    # Some links to pdfs are behind another link - manually alter list of pdf links
    pdf_letters = links[21:]
    for i, link in enumerate(pdf_letters):
        if i < 5:
            pdf_letters[i] = link[:4] + 'pdf.pdf'
        if i == 5:
            pdf_letters[i] = link[:4] + 'ltr.pdf'

    # Download pdf letters and extract text
    r = requests.get(url+pdf_letters[0], stream=True, timeout=5)

    with open('/home/ben/Code/BuffettLetters/test.pdf', 'wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    main()

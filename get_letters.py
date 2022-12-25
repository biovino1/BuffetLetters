"""================================================================================================
This script accesses each 'Letter to Shareholders' from Berkshire Hathaway's online archive and
writes them to individual text files.

12/24/22   Ben Iovino   BuffettLetters
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


def html_to_text(url, links, headers):
    """=============================================================================================
    This function takes a url and list of sublinks that lead to html webpages and writes their
    text content to an individual file.

    :param url: root url
    :param links: list of links leading to individual webpages
    :param headers: headers used for requests
    ============================================================================================="""

    # Create directory for html letters
    if not os.path.exists('html_letters'):
        os.mkdir('html_letters')

    # Iterate over each webpage
    for i, link in enumerate(links):

        # Get content of webpage, parse with beautiful soup
        request = requests.get(url+link, headers=headers, timeout=5)
        letter = BeautifulSoup(request.text, 'html.parser')
        letter = letter.get_text()

        # Write to file as is
        with open(f'html_letters/{i+1977}.txt', 'w', encoding='utf8') as file:
            file.write(str(letter))


def pdf_to_text(url, links):
    """=============================================================================================
    This function takes a url and list of sublinks that lead to pdf webpages and writes their text
    content to an individual file.

    :param url: root url
    :param links: list of links leading to individual webpages
    ============================================================================================="""

    # Create directory for pdf letters
    if not os.path.exists('pdf_letters'):
        os.mkdir('pdf_letters')

    # Iterate over each webpage
    for i, link in enumerate(links):

        # Download pdf letters and extract text
        request = requests.get(url+link, stream=True, timeout=5)
        with open('/home/ben/Code/BuffettLetters/letter.pdf', 'wb') as file:
            file.write(request.content)

        # Extract text from pdf
        text = ''
        with open('letter.pdf', 'rb') as pdf:
            PdfReader = PyPDF2.PdfReader(pdf)
            for page in PdfReader.pages:
                text += page.extract_text()

        # Write text to file
        with open(f'pdf_letters/{i+1998}.txt', 'w', encoding='utf8') as file:
            file.write(text)
        os.remove('letter.pdf')


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
    html_to_text(url, html_letters, headers)

    # Some links to pdfs are behind another link - manually alter list of pdf links
    pdf_letters = links[27:]
    more_pdf = ['1998pdf.pdf', 'final1999pdf.pdf', '2000pdf.pdf',
        '2001pdf.pdf', '2002pdf.pdf', '2003ltr.pdf']
    pdf_letters = more_pdf + pdf_letters

    # Get letters from pdf webpages (these pages don't require a user-agent)
    pdf_to_text(url, pdf_letters)

if __name__ == '__main__':
    main()

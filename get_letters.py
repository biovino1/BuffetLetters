"""This script gets the text from each 'Letter to Shareholders' from Berkshire Hathaway's online
archive, cleans them, and writes them all to one text file.

__author__ = 'Ben Iovino'
__date__ = '12/26/22'
"""

import os
import re
import requests
import fitz
import nltk
from bs4 import BeautifulSoup


def get_links(url: str, headers: dict) -> list:
    """Returns a list of the desired links from the given url.

    :param url: root url
    :param headers: headers used for requests
    :return: list of links
    """

    # Request url and parse html
    page = requests.get(url, headers=headers, timeout=5)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get links to individual letters
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    links = links[1:-1]  # First and last links are irrelevant

    return links


def clean_letter(text: str):
    """Cleans and writes a body of text to a file.

    :param text: string
    """

    # Remove special characters
    text = re.sub('[^a-zA-Z0-9\n\.]', ' ', text)

    # Tokenize words to remove spaces and newline characters
    text = ' '.join(nltk.word_tokenize(text))

    # Letters have contractions separated - use re.sub to fix
    regexes = ((" s ", "'s "), (" ve ", "'ve "), (" re ", "'re "),
        (" m ", "'m"), (" ll ", "'ll "), (" t ", "'t "), (" d ", "'d"))
    for reg in regexes:
        text = re.sub(reg[0], reg[1], text)

    # Some letters have graphs in beginning and letters after Buffett's - remove these
    beg = re.search("To the Shareholders|To the Stockholders", text).span()[0]
    end = re.search("Warren E. Buffett| Warren E. Buff ett", text).span()[1]
    text = text[beg:end]

    # Append to file, each letter is one line in the same text file
    with open('data/letters.txt', 'a', encoding='utf8') as file:
        file.write(str(text)+'\n')


def html_to_text(url: str, links: list, headers: dict):
    """Writes text content of a list of html webpages to individual text files.

    :param url: root url
    :param links: list of links leading to individual webpages
    :param headers: headers used for requests
    """

    # Get content of webpage, parse html with beautiful soup
    for link in links:
        request = requests.get(url+link, headers=headers, timeout=5)
        soup = BeautifulSoup(request.text, 'html.parser')
        letter = soup.get_text()

        # Clean and write to file
        clean_letter(letter)


def pdf_to_text(url: str, links: list):
    """Writes text content of a list of pdf webpages to individual text files.

    :param url: root url
    :param links: list of links leading to individual webpages
    """

    # Download pdf letters and extract text
    for link in links:
        request = requests.get(url+link, stream=True, timeout=5)
        with open('/home/ben/Code/BuffettLetters/letter.pdf', 'wb') as file:
            file.write(request.content)

        # Extract text from pdf
        text = ''
        with open('letter.pdf', 'rb') as pdf:
            doc = fitz.open(pdf)
            for page in doc:
                text += page.get_text()

        # Clean and write to text file, delete pdf file
        clean_letter(text)
        os.remove('letter.pdf')


def main():
    """Defines a url and writes the text content from each of its links to a text file.
    Some links are to html webpages, others are to pdfs.
    """

    # Set user-agent hearder for requests (UA below sent by personal machine)
    headers = {'User-Agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'}

    # Get all links from url
    os.makedirs('data/')
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

    # Download S&P 500 annual return since 1926
    url = 'https://www.slickcharts.com/sp500/returns/history.csv'
    request = requests.get(url, headers=headers, timeout=5)
    with open('data/sp500.csv', 'wb') as file:
        file.write('year,performance\n'.encode('utf8'))
        file.write(request.content)


if __name__ == '__main__':
    main()

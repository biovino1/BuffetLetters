# BuffettLetters
Every year, Warren Buffett releases a 'Letter to Shareholders' to Berkshire Hathaway investors in which he covers the performance of the company and the market as a whole. The goal of this project is to determine similarity between these letters using various natural language processing techniques and see if predictions can be made about the stock market the year following a letter is published using the S&P 500 as an indicator for market performance.

get_letters.py can be called to reproduce all of the data used in this repo - letters.txt, which contains each year's letter (from 1977 to 2021) on a single line, and sp500.csv, which contains the S&P 500 annual returns since 1926. Some cleaning is performed by this script as well, but more is performed by the ipynb files when necessary.

similarity.ipynb processes these letters and creates embeddings to compare similarity between them. The first technique, count vectorization, shows no real similarity between letters. The second technique, term frequency-inverse document frequency shows even less similarity between letters.

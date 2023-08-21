**************************************************************************************************************
# Comparing Market Performance To Warren Buffett's Letters To Shareholders
**************************************************************************************************************

Every year, Warren Buffett releases a 'Letter to Shareholders' to Berkshire Hathaway investors in which he covers the performance of the company and the market as a whole. The goal of this project is to determine similarity between these letters using various natural language processing techniques and see if predictions can be made about the stock market the year following a letter is published using the S&P 500 as an indicator for market performance.

**************************************************************************************************************
# Data
**************************************************************************************************************

get_letters.py can be called to reproduce all of the data used in this project - letters.txt, which contains each year's letter (from 1977 to 2021) on a single line, and sp500.csv, which contains the S&P 500 annual returns since 1926. Some cleaning is performed by this script as well, but more is performed by the notebook files when necessary.

**************************************************************************************************************
# Similarity Findings
**************************************************************************************************************

similarity.ipynb processes these letters and creates embeddings to compare similarity between them. The first technique, count vectorization, shows no useful similarity between letters. The second technique, term frequency-inverse document frequency shows even less similarity between letters. The third technique, training a Doc2Vec model, again showing no useful similarty between letters. 

Letters that are written in similar years are found to be the most similar to each other. This may in part be because of Buffett's writing style changing throughout the years and years written in similar times would have the most similar styles. Letters also change drastically in length - the first several and last several letters are extremely short compared to all of the other letters. Longer letters presumably have more information and larger vocabularies, which would make them more difficult to compare to other letters.

**************************************************************************************************************
# Predicting Sentiment And Comparing To Market Performance
**************************************************************************************************************

prediction.ipynb trains two different neural networks - a basic ANN and an LSTM - to predict the overall sentiment of each letter. Each model was trained on IMDB reviews. Given their length, a few sentences, we predicted the sentiment of each sentence in Buffett's letters and averaged the results to get the overall sentiment.

The LSTM appeared to perform better than the ANN, but there was not a consistent correlation between predicted sentiment and market performance. Training data that more accurately reflects the language used in Buffett's letters may improve the results, as well building more complex models or fine tuning pre-trained models on some
of the letters. 
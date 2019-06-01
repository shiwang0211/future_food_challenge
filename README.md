# Data Competition: Future Food Challenge
Link to the competition: https://tianchi.aliyun.com/competition/entrance/231705/introduction. We are rank **5** out of **661** teams.

# Context
This competition requires developing an algorithm to identify food safety incidents from a bunch of news, and to group news covering the same food safety event into clusters. The results are evaluated based on:
- how well can the teams distinguish between relevant and other news items by the recall/ precision/ accuracy.
- how well can the teams distinguish between the individual events

# Approach
In this challenge we are asked to identify food-safety related news and to group the news that covers the same event. Learning algorithm should be proposed based on a good understanding of the training set, and our task is to perform the clustering task on all the news in the test set.

There are several challenges in the task, and we proposed specific strategies as follows to address them,

-   **There is a mixture of food safety related news and irrelevant news in the test set.** Without excluding those irrelevant news, it would be hard to achieve good model performance by directly applying any clustering techniques. So the strategy is to develop an understanding of what a food-safety related news is from the training set where each news is labelled, and a supervised model is establish to identify if a specific piece of news is food-safety related or not.
-   **No prior information on number of topics and what the events would be covered.** While off-the-shelf clustering and topic modelling technique can be quickly applied to the test set, model performance is poor because the format of tweets are pretty messy and different usage of words may be found for the same event. Manual review is therefore performed after model implementation to refine the keywords and determine number of topics in an iterative manner.
-   **Limited information with tweet title and abstract.** After investigating on the tweet titles and abstracts manually, we found a number of tweets with little useful information in the text itself, and rich information in several other tweet-related info, like external links, the tweet that the user replied to, user names, etc. All these useful information will be pulled by Twitter API or web scraping.
-  **Different events across training and test set.** In the task, the training set has fewer samples than test set with different events. A binary classification model based on TF-IDF matrix of the corpus turned out to be not useful to determine whether the news is food-safety relevant or not. While model performs well on train set, it gives poor performance on test set as the keywords can change with specific events, and become no longer applicable to test set. Therefore other tweet-related information and external link title are added to enhance model generalization. 

## Overall workflow


<table>
  <tr>
   <td><strong>Adding External Data</strong>
   </td>
  </tr>
  <tr>
   <td>Extract Info through Tweet API
   </td>
  </tr>
  <tr>
   <td>Web Scraping on External Link
   </td>
  </tr>
</table>


⬇️


<table>
  <tr>
   <td><strong>Text Mining</strong>
   </td>
  </tr>
  <tr>
   <td>Tokenization
   </td>
  </tr>
  <tr>
   <td>Data Cleaning
   </td>
  </tr>
  <tr>
   <td>Feature Engineering
   </td>
  </tr>
</table>


⬇️


<table>
  <tr>
   <td><strong>Binary Classification</strong>
   </td>
  </tr>
  <tr>
   <td>Apply Logistic Regression
   </td>
  </tr>
  <tr>
   <td>Export News (that predicted to be food-safety relevant)
   </td>
  </tr>
</table>


⬇️


<table>
  <tr>
   <td><strong>Topic Modelling</strong>
   </td>
  </tr>
  <tr>
   <td>Apply LDA (Latent Dirichlet Allocation)
   </td>
  </tr>
  <tr>
   <td>Refine # of topics and words
   </td>
  </tr>
</table>

## External Data
- Extract Tweet Info: 
Tweet API ([https://developer.twitter.com/en.html](https://developer.twitter.com/en.html)) and Twython package ([https://twython.readthedocs.io/en/latest/](https://twython.readthedocs.io/en/latest/)) are used to extract tweet-related information for each tweet in test set. See appendix for example.

- Extract page title from external link in tweet abstract:
standard urllib and BeautifulSoup packages are used to extract the page title. See below for example.

## Tokenization:
standard spacy library is used to 
- remove stop words, punctuations, numbers, space and other non-alpha characters. 
- perform lemmatization on each individual word.

## Data Preprocessing:
- Standard collections. Counter is used to get statistical word frequency.  
- The garbage words are defined as words with count frequency less than 3 times,  or the length of word shorter than 3 (such as lo, ta, etc.) . These garbage words are removed from text.
- **Binary classification model** (to determine whether a news is food-safety related or not): standard logistic regression from scikit learn with manually generated features including:

## Tweet-related Featue
*   Hashtags: (relevant news are more likely to have hashtags like #Recall, #SmartNews, etc.)
*   Mentions: (relevant news are more likely to have mentions like @googlenews)
*   UserNames: (a tweet with username including ‘News’ is more likely to be relevant news) 
*   Medias (relevant news are more likely to have figures with the tweet)

## NLP features
*   Length of sentence: (relevant news tends to have a longer sentence)	
*   Punctuation: (relevant news are less likely to include many question marks) 
*   Words: (relevant news are more likely to have include words like ‘recall’, ‘alert’, ‘allergy’, ‘outbreak’, etc.	
*   Proper nouns: (relevant news tends to include more proper nouns (NNP) that represents people, places, things, etc.)
*   Nouns (sentences including ‘I, you, me, we, they, it’ are unlikely to be relevant news)

## Topic Modelling:
standard gensim is used to 
- get the dictionary and the bag of words by using gensim.corpora.Dictionary.
- get the topic distribution and keywords of each topic by using gensim.models.LdaModel and the core parameter settings are as follow:
  - num_topics: determined by 3)
  - alpha: “auto”
  - passes: 100
  - random_state: 42	

- calculate the coherence value to get the lda model which is the best number of topics by using gensim.models.CoherenceModel and the core parameter settings are as follow: coherence: “c_v”

# Results
Our analysis detected 11 news events in test set, and the top events description are as follows:
- Pillsbury Flour has been recalled due to salmonella concerns
- Butterball Raw ground turkey products has been recalled due to salmonella contamination
- Boyardee Chicken and rice products have been recalled due to misbranding and undeclared allergens
- French Cheese has been recalled due to E. coli, etc.

# Future work
- The result of topic detection with some news is not good, probably because the LDA model is not the optimal solution in dealing with short text. Further study is needed to identify topic model that fits better for short text. 
- There are several manual processing steps involved, and we hope to find a more automated data processing method so that the model could better scale and generalize to a new set of events.
- Some records of the datasets are non-English sentences (e.g., Spanish, Japanese, etc.) We have removed these sentences because of the small proportion. Given more time, we may try language detection and automatic translation to take care of these foreign tweets. 

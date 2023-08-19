
# import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create lists to store scraped news urls, headlines and text
url_list = []
date_time = []
news_text = []
headlines = [] 

for i in range(1,3): #parameters of range function correspond to page numbers in the website with news listings
    #get the list of unique urls in the page
    url = 'https://oilprice.com/Energy/Crude-Oil/Page-{}.html'.format(i)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")  #using beautiful soup to get all text from html page
    for links in soup.find_all('div', {'class': 'categoryArticle'}):
        for info in links.find_all('a'):
            if info.get('href') not in url_list:   #there can be many same urls , so avoid them
                url_list.append(info.get('href'))

for www in url_list:
    #access each url
    headlines.append(www.split("/")[-1].replace('-',' ')) #the end part of the url itself contains Heading, so we are spliting on the basis of / and taking the last element and replacing the - with ''
    request = requests.get(www)
    soup = BeautifulSoup(request.text, "html.parser")  #again we are establishing the connection and going the page of that particulr url and creating the object of the beautiful soup
    
    #store date and time of publication of the article
    for dates in soup.find_all('span', {'class': 'article_byline'}):  #this loop will loop through every single element in the span tag for the class article_byline
        date_time.append(dates.text.split('-')[-1])
    
    #store the text of the news
    temp = []
    for news in soup.find_all('p'): #loopint through the object of the Beautifulsoup which contains entire html page and finding all paragraph
            temp.append(news.text)  #and appending that in temp list which contains a lot of things that we dont require
    
    #identify the last line of the news article
    for last_sentence in reversed(temp):  #looping in reverse order
        if last_sentence.split(" ")[0]=="By" and last_sentence.split(" ")[-1]=="Oilprice.com":   #making the sentence which starts with by and ends with oilprice.com as our last sentence
            break                       
        elif last_sentence.split(" ")[0]=="By":
            break
    
    #prune non news related text from the scraped data to create the news text
    joined_text = ' '.join(temp[temp.index("More Info")+1:temp.index(last_sentence)])  #taking the body of the article after more info line
    news_text.append(joined_text)


# save news text along with the news headline in a dataframe      
news_df = pd.DataFrame({ 'Date' : date_time,
                         'Headline': headlines,
                         'News': news_text,
                       })

# use VADER to perform sentiment analysis on stored news articles
analyser = SentimentIntensityAnalyzer()  #initiating a sentiment object

def compound_score(text):  #all we need is only the compound score
   return analyser.polarity_scores(text)["compound"]   #extracting the compound score from the text/news
  
news_df["sentiment"] = news_df["News"].apply(compound_score) #now applying the above function to the news column of the dataframe to get the sentiment score


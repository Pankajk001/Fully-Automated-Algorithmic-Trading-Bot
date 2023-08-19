
# import necessary libraries
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import pickle

data = pd.read_csv("24-CrudeOil_News_Articles  Data got from Web Scrapping.csv", encoding = "ISO-8859-1")

X = data.iloc[:,1] # extract column with news article body

# tokenize the news text and convert data in matrix format
vectorizer = CountVectorizer(stop_words='english')
X_vec = vectorizer.fit_transform(X)
print(X_vec) # Scipy sparse matrix
pickle.dump(vectorizer, open("vectorizer_crude_oil", 'wb')) # Save vectorizer for reuse
X_vec = X_vec.todense() # convert sparse matrix into dense matrix

# Transform data by applying term frequency inverse document frequency (TF-IDF) 
tfidf = TfidfTransformer() #by default applies "l2" normalization
#X_tfidf = tfidf.fit_transform(X_vec)

X_vec_array = np.asarray(X_vec)  #now fit_transform method expects NumPy array istead of NumPy Matrix, thats why converting this into array

# Fit and transform the data
X_tfidf = tfidf.fit_transform(X_vec_array)
X_tfidf = X_tfidf.todense()


##################Apply Naive Bayes algorithm to train data####################

# Extract the news body and labels for training the classifier
X_train = np.array(X_tfidf[:66,:])
Y_train = data.iloc[:66,2]

# Train the NB classifier
clf = GaussianNB().fit(X_train, Y_train) 
pickle.dump(clf, open("nb_clf_crude_oil", 'wb')) # Save classifier for reuse


#The strange characters you're seeing when opening the file in MS Word are likely 
#due to the fact that classifier objects are serialized binary data, 
#which is not human-readable. When opened in a text editor or word processor, 
#the binary data can be misinterpreted and displayed as unusual characters. 
#To work with the classifier, you need to load it back into a Python environment 
#using the appropriate library, as shown in the loading example above.



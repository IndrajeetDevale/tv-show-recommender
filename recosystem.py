import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_title_from_index(index):
	return df[df.index == index]["tv_series"].values[0]

def get_index_from_title(tv_series):
	return df[df.tv_series == tv_series]["index"].values[0]
cv = CountVectorizer()
#read CSV file
df = pd.read_csv("tv_ratings4.csv")
print(df.columns)

#pick features
features = ['genres','cast','imdb', 'year', 'description']
for feature in features:
	df[feature] = df[feature].fillna('')

#create df column
def combine_features(row):
	try:
		return row['genres'] + " " + row['cast'] + " " + row['description']
	except:
		print ("Error:", row)
df["combined_features"] = df.apply(combine_features, axis = 1)

print ("Combined Features:", df["combined_features"].head())	


count_matrix = cv.fit_transform(df["combined_features"])
cosinsim = cosine_similarity(count_matrix)

tv_user_likes = "The Big Bang Theory"

tv_index = get_index_from_title(tv_user_likes)
similar_tv = list(enumerate(cosinsim[tv_index]))

sorted_similar_tv = sorted(similar_tv, key = lambda x:x[1], reverse = True)

i=0
for tv in sorted_similar_tv:
	print (get_title_from_index(tv[0]))
	i = i+1
	if i>10:
		break

#print(cv_fit.toarray())
#cosinsim = cosine_similarity()

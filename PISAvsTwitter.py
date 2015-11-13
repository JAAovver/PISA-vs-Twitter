import json
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy import stats
import numpy as np
import math

def JsonToList(readfile):
	tweets_data = []
	tweets_file = open(readfile, "r")
	for line in tweets_file:
		try:
			tweet = json.loads(line) #json attribute-value pairs for each tweet
		except: #takes all kinds
			continue
		if ('text' and 'country' and 'place') in tweet: #make sure there's a country identifier and text
			tweets_data.append(tweet)
	return tweets_data

def main():
	pisa_frame = pd.read_csv('pisa_scores.csv',index_col=0) #countries' pisa scores
	AllishTweets = JsonToList('all_words3.txt') # tweet volume for normalization
	PisaTweets = JsonToList('pisa_words2.txt') # 'intellectual' tweets

	PisaTabled = pd.DataFrame()
	AllishTabled = pd.DataFrame()
    
    # look at country of origin
	PisaTabled['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, PisaTweets)
	AllishTabled['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, AllishTweets)

    # how many tweets? Make a series of that for the different countries
	PisaByCtry = PisaTabled['country'].value_counts()
	AllishByCtry = AllishTabled['country'].value_counts()
	
	# take the counts, ""join"" as dataframe and also add in pisa scors
	PisaEtAll = pd.concat([PisaByCtry,AllishByCtry,pisa_frame],axis=1, join='inner')

	pisa_score = PisaEtAll['score'] # read from that dataframe column
	tweet_score = PisaEtAll[0]/PisaEtAll[1] # calculate frequency of intellectual tweets

    # prepare for scipy linregress
	X = np.array(pisa_score)
	Y = np.array(tweet_score)	
	slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
	R2 = r_value**2
	print 
	print 'The slope is: ', slope
	print 'The intercept is: ', intercept
	print 'The r-squared value is: ', R2
	# z = np.polyfit(X,Y,2)
	# f = np.poly1d(z)
	# xplot = np.linspace(X[0],X[-1],50)
	# yplot = f(x_plot)

	xplot = range(600)
	yplot = [intercept+slope*i for i in range(600)]
	area = [PisaEtAll[1][i] for i in range(len(pisa_score))]
	colors = np.linspace(0.1,1,len(pisa_score))
	plt.scatter(pisa_score,tweet_score, s=np.array(area), c=colors, alpha=0.5)
	plt.plot(xplot,yplot,linestyle='--',linewidth=2,color='r')
	plt.xlabel('Raw PISA Score')
	plt.ylabel('Percent of texts containing PISA-like words')
	plt.title('Culture of intellectual discourse vs. PISA scores')
	plt.axis([350, 525, 0, 1])
	plt.show()

if __name__ == '__main__':
	main()

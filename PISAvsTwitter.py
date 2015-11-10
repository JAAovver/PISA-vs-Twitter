import json
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy import stats
import numpy as np
import math

read_file = 'pisa_words2.txt'
tweets_data_path = read_file
# tweets_data_path = 'all_words3.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line) #json attribute-value pairs for each tweet
    except:
        continue
    if ('text' and 'country' and 'place') in tweet: #make sure there's a country identifier and text
        tweets_data.append(tweet)

tweets = pd.DataFrame()

tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

tweets_by_country = tweets['country'].value_counts()
print tweets_by_country[:20]
normalizers = [2258.0, 446.0,1,99.0,169.0,53.0,172.0,1,1,34.0,52.0] #representation of all tweets - pisa_words2.txt/all_words3.txt
tweet_score = [100*tweets_by_country[i]/normalizers[i] for i in range(11)]
print tweets_by_country[:20]

del tweet_score[2] #no pisa score for phillipines
del tweet_score[6] #no count score for spain
del tweet_score[6] #no pisa score for india

pisa_score = [481,494,518,391,495,421,375,485] #PISA scores from http://www.oecd.org/pisa/keyfindings/pisa-2012-results-overview.pdf

X = np.array(pisa_score)
Y = np.array(tweet_score)
slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
R2 = r_value**2
print 
print 'The slope is: ', slope
print 'The intercept is: ', intercept
print 'The r-squared value is: ', R2


xplot = range(600)
yplot = [intercept+slope*i for i in range(600)]
area = [normalizers[i] for i in range(8)]
colors = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
colors = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 0.2, 0.4, 0.6])
plt.scatter(pisa_score,tweet_score, s=np.array(area), c=colors, alpha=0.5)
plt.plot(xplot,yplot,linestyle='--',linewidth=2,color='r')
plt.xlabel('Raw PISA Score')
plt.ylabel('Percent of texts containing PISA-like word')
plt.title('Culture of intellectual discourse vs. PISA scores')
plt.axis([350, 525, 0, 75])
plt.show()
















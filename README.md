# PISA-vs-Twitter
How well does the content of country's tweets predict its PISA scores? 

In this weekend project, I learned how to stream tweets and filter for key words. So I ran this line of code in my tweepy streamer file:

```
stream.filter(track = ['artist','book','poem','poet','author','learn','science','physics','engineering','math'])
```

This just sets aside all tweets containing any members of that list of words. Why? I want to check if the frequency with this words appear relate to the level of education of a society. Whether 'physics' is mentioned in a tweet in a positive or negative way, maybe the fact that it's being discussed and considered at all means that it's on the public consciousness and indicates at least a partial interest in these intellectual areas. 

Before I go on, quick disclaimer: this was a weekend project and the existence of this citationless repository should not be taken as a claim of primacy.

Now I'll reference 'PISAvsTwitter.py'. The program either reads in a `pisa_words` or `all_words` file. The former is a list of tweets containing the intellectual words I care about, the latter is used for normalization and contains almost all tweets generated.

I break apart the JSON-formatted structure like so

```
tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line) #json attribute-value pairs for each tweet
    except:
        continue
    if ('text' and 'country' and 'place') in tweet: #make sure there's a country identifier and text
        tweets_data.append(tweet)
```

and then create, in this case, just a one-column pandas dataframe `tweets = pd.DataFrame()`. I then filter by country and count the number of tweets coming from each country. I normalize this by the number of tweets contained in the normalization set (from having previously run this on `all_words`), delete entries where there's missing data.

I then use a scipy linear regression to see how well the PISA scores track the intellectual tweet frequency and plot the results. The size of the bubbles on the scatter plot relate to the amount of tweets coming from a country. 

I included a result I got from processing ~1 GB of tweets over a few-hour time frame.



import got
import sys,getopt,datetime,codecs
import os

def get_tweets(twitter_handles, begin_date, end_date, outputFileName):
	if os.path.exists(outputFileName):
		outputFile = codecs.open(outputFileName, "a", "utf-8")	
		print(outputFileName+' already exists. New data will be appended.')
	else:
		print('File does not exist. Creating new file, '+outputFileName)
		outputFile = codecs.open(outputFileName, "w+", "utf-8")
		outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
	for handle in twitter_handles:
		try:
			print('Receiving tweets for '+ handle)
			tweetCriteria = got.manager.TweetCriteria()
			tweetCriteria.username = handle
			tweetCriteria.since = begin_date
			tweetCriteria.until = end_date
			
			
			def receiveBuffer(tweets):
				for t in tweets:
					outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
				outputFile.flush()
				print('More %d saved on file...\n' % len(tweets))

			got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		except:
			print('ERROR: Failed for '+handle)
		finally:
			print('Done for '+ handle)

	print('Done. Output file generated "%s".' % outputFileName)		
	outputFile.close()

def main():
	from parameters import handles, begin_date, end_date, filename
	get_tweets(handles, begin_date, end_date, filename)

if __name__ == '__main__':
	main()
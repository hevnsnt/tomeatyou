#import required modules:
from twython import Twython
import time
import random
import argparse

def writelog(message):
	if verbose:print(message)
	output = open(logfile, 'a')
	logstring = "%s,%s\n" % (str(time.strftime('%X %x %Z')), message.encode('ascii', 'ignore'))
	output.write(logstring)
	output.close

def twmeatit(tweet):
	if len(tweet) <= 140:
		try:
			writelog("Getting ready to tweet: %s" % tweet)
			if not testMode:twitter.update_status(status=tweet)
			writelog('Tweet was successful')
		except Exception, e:
			writelog('Something went wrong with tweet, error %s' % e)
			writelog('Choosing another tweet')
			meatmentions(readfile(infile))
	else:
		writelog('Chosen tweet was > 140 Chars, choosing another one...')
		meatmentions(readfile(infile))

def meatme(statusMsg):
	writelog('Choosing Random Twitter String')
	randTwitterInt = random.randrange(0, int(statusMsg['search_metadata']['count']),1) 
	statusMsgText = statusMsg['statuses'][randTwitterInt]['text']
	user = statusMsg['statuses'][randTwitterInt]['user']['screen_name']
	if "met" not in statusMsgText and "meet" not in statusMsgText:
		writelog('"meet" not found, lets try again:')
		meatmentions(readfile(infile))
	if "met" in statusMsgText:
		writelog('Replacing met with meated in text: %s' % statusMsgText)
		statusMsgText = statusMsgText.replace('met', 'meated')
	if "meet" in statusMsgText:
		writelog('Replacing meet with meat in text: %s' % statusMsgText)
		statusMsgText = statusMsgText.replace('meet', 'meat')
	tweet = "RT @%s: %s" % (user, statusMsgText)
	twmeatit(tweet)

def meatmentions(searchText):
	writelog('Getting Twitter Search Results')
	meatme(twitter.search(q='"' + searchText + '"'))

def readfile(infile): # This is step one: 
	writelog('Reading %s as input' % infile)
	data = filter(bool, [line.strip() for line in open(infile, 'r')]) # This reads the file in line by line into a list, stripping blank lines
	randInt = random.randrange(0, len(data),1) # This gets a random integer that ranges from 0 to the number of lines in the text
	return data[randInt] # Returns the search text that we are going to search for

#-------------------Get command line input----------------------------------
parser = argparse.ArgumentParser(description='Silly bot that likes to meat people', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v', action='store_true', dest='verboseMode', help='Verbose mode will direct output to screen as well as logfile\n\n')
parser.add_argument('-t', action='store_true', dest='testMode', help='Test mode wont actually tweet\n\n')
#-------------------End command line input----------------------------------

#-------------------Init global vars----------------------------------
results = parser.parse_args()
testMode = results.testMode
verbose = results.verboseMode
logfile = '/root/tomeatyou/logfile.log'
infile = '/root/tomeatyou/search-text.txt'
#-------------------Init global vars----------------------------------


#-------------------Need to init your twitter oauth----------------------------------
consumer_key='bw42b0kSIojsfrvhrpeew' # Replace with yours, this is just gibberish 
consumer_secret='6uU87zRdPhDlj7kCNISMHVZAsRtgHrk9xr5pkfRmA58' # Replace with yours, this is just gibberish 
access_token_key='1026881880-NRFJhKKwBxxnTqJYhgVjBOF0iCM2IywVhEvwaAaa' # Replace with yours, this is just gibberish 
access_token_secret='aiBk4ijeH7L7kcJEGLRhbm-SSkS1qRRYXj0qLinSc' # Replace with yours, this is just gibberish 
twitter = Twython(consumer_key, consumer_secret, access_token_key, access_token_secret)  # This authorize our bot, and will be our interface into the Twython functions
#-------------------Need to init your twitter oauth----------------------------------

writelog('Script Started')
if verbose:writelog('####################### Verbose Mode Detected! #######################')
if testMode:writelog('####################### Test Mode Detected, I will not tweet #######################')
#meatmentions(readfile(infile))

try:
	meatmentions(readfile(infile))
except Exception, e:
	writelog('Error %s' % e)
	meatmentions(readfile(infile))

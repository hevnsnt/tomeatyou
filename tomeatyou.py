#!/usr/local/bin/python
#-------------------imports----------------------------------------
from twython import Twython # Needed for twitter
import time # Needed for log writes
import random # Needed to choose random number
import argparse # Needed to parse commandline arguments
import config # Needed for configuration variables (config.py)
#-------------------imports----------------------------------------

#-------------------Functions----------------------------------------
def postsPast(message):
	writelog("Checking to see if we have previously posted this particular message")
	pastMessages = filter(bool, [line.strip() for line in open(pastposts, 'r')]) # This reads the file in line by line into a list, stripping blank lines
	if message in pastMessages: # If we have previously posted that text
		writelog("Duplicate message found, restarting search") # Log write
		return True # Return that it was true that we found a match
	else:
		pastpostsWriter = open(pastposts, 'a')
		pastpostsWriter.write(message.encode('ascii', 'ignore'))
		pastpostsWriter.close()
		return False

def writelog(message):
	'''This function writes to a logfile, and if verbose is true, it will also print
	the message to the screen'''
	if verbose:print(message) # Check to see if we are in verbose mode, if so, print the message to the screen
	output = open(logfile, 'a') # Open the logfile for writing in append mode (so we dont overwrite previous log entries)
	logstring = "%s,%s\n" % (str(time.strftime('%X %x %Z')), message.encode('ascii', 'ignore')) # Get the time (in HH:MM:SS MM/DD/YY CDT format), 
	# and convert the message to straight ASCII (as twitter msgs can contain unicode chars)
	output.write(logstring) # Write the string to the file 
	output.close # Close the file

def twmeatit(tweet):
	'''This function does the tweeting.  First it checks to make sure that the message isn't over 140
	chars, then checks to see if we are in Test Mode, and if passed both will tweet'''
	if len(tweet) <= 140: # Make sure the full text we intend to tweet is less than 140 chars (including the RT: + Username + Message)
		try:
			writelog("Getting ready to tweet: %s" % tweet) # Write to the logfile
			if not testMode:twitter.update_status(status=tweet) # Check to see if we are in test mode, and if not send the tweet
			writelog('Tweet was successful') # We know it was successful, because if there was an error, it would have been caught below
		except Exception, e: # If we fail sending to twitter for any reason, catch the exception here, store error message in variable 'e'
			writelog('Something went wrong with tweet, error %s' % e) # Write to the log with the error message
			writelog('Choosing another tweet') # Log write
			meatmentions(readfile(infile)) # Since something went wrong; Restart the entire process and choose a completely new tweet
	else:
		writelog('Chosen tweet was > 140 Chars, choosing another one...') # Log write
		meatmentions(readfile(infile)) # Since the message was over 140 chars, restart the entire process and choose a completely new tweet

def meatme(statusMsg):
	''' Expects a dictionary containing Twitter search results, then chooses a random one, and changes it'''
	writelog('Choosing Random Twitter String') # Log write
	randTwitterInt = random.randrange(0, int(statusMsg['search_metadata']['count']),1) # Get the number of results in the dictionary (count), and then chooses a random number from 0-that.
	statusMsgText = statusMsg['statuses'][randTwitterInt]['text'] # Choose the random text we are going to edit
	user = statusMsg['statuses'][randTwitterInt]['user']['screen_name'] # Get ther username of the random text
	if "met" not in statusMsgText and "meet" not in statusMsgText: # As twitter search is case in-sensitve, this is a bug fix to handle the case bug (MEET != meet)
		writelog('"meet" not found, lets try again:') # Log write
		meatmentions(readfile(infile)) # Since we didnt match successfully, Restart the entire process and choose a completely new tweet
	if "met" in statusMsgText:
		writelog('Replacing met with meated in text: %s' % statusMsgText) # Log write
		statusMsgText = statusMsgText.replace('met', 'meated') # Replace 'met' with 'meated' in the tweet text
	if "meet" in statusMsgText:
		writelog('Replacing meet with meat in text: %s' % statusMsgText) # Log write
		statusMsgText = statusMsgText.replace('meet', 'meat') # Replace 'meet' with 'meat' in the tweet text (will cover meeting, etc)
	if postsPast(statusMsgText) == False:
		tweet = "RT @%s: %s" % (user, statusMsgText) # Setup our complete tweet string
		twmeatit(tweet) # Send tweet string to twmeatit function for tweeting
	else:
		meatmentions(readfile(infile)) # Since we have previously posted this; Restart the entire process and choose a completely new tweet

def meatmentions(searchText):
	'''This function will search twitter for our search text, and pass the dictionary results to meatme (text processing function)'''
	writelog('Getting Twitter Search Results') # Log write
	meatme(twitter.search(q='"' + searchText + '"')) # This searches twitter for our text (in ""'s) and returns a dictionary of results, then passes that dict to meatme funct

def readfile(infile):
	'''This is step one: Return a list of search terms out of the search text in-file'''
	writelog('Reading %s as input' % infile) # Log write
	data = filter(bool, [line.strip() for line in open(infile, 'r')]) # This reads the file in line by line into a list, stripping blank lines
	randInt = random.randrange(0, len(data),1) # This gets a random integer that ranges from 0 to the number of lines in the text
	return data[randInt] # Data is a list of search terms, this chooses a random one from that list, and returns it as a string.
#-------------------Functions----------------------------------------

#-------------------Get command line input----------------------------------
parser = argparse.ArgumentParser(description='Silly bot that likes to meat people', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v', action='store_true', dest='verboseMode', help='Verbose mode will direct output to screen as well as logfile\n\n')
parser.add_argument('-t', action='store_true', dest='testMode', help='Test mode wont actually tweet\n\n')
#-------------------End command line input----------------------------------

#-------------------Init global vars----------------------------------
results = parser.parse_args() # Parse the command line arguements and save to variable 'results'
testMode = results.testMode # if the user sent -t, testMode will be True (otherwise false)
verbose = results.verboseMode # if the user sent -v, verbose will be True (otherwise false)
logfile = config.LOGFILE # Get logfile file location from config file
infile = config.INFILE # Get search text file location from config file
pastposts = config.POSTSPAST # Get postsPast file location from config file
#-------------------Init global vars----------------------------------


#-------------------Need to init your twitter oauth----------------------------------
consumer_key = config.CONSUMER_KEY # Get Consumer Key from config file 
consumer_secret = config.CONSUMER_SECRET # Get Consumer Secret from config file 
access_token_key = config.ACCESS_TOKEN_KEY # Get Access Token Key from config file 
access_token_secret = config.ACCESS_TOKEN_SECRET # Get Access Token Secret from config file 
twitter = Twython(consumer_key, consumer_secret, access_token_key, access_token_secret)  # This authorize our bot, and will be our interface into the Twython functions
#-------------------Need to init your twitter oauth----------------------------------

writelog('Script Started') # Log write
if verbose:writelog('####################### Verbose Mode Detected! #######################') # Check to see if verbose, if so log write (will also write to screen)
if testMode:writelog('####################### Test Mode Detected, I will not tweet #######################') # Check to see if testMode, if so log write

try:
	meatmentions(readfile(infile)) # This initiates the main program, with the chosen search term returned from readfile()
except Exception, e: # Catches any main exceptions
	writelog('Error %s' % e) # Log write (with error message in log)
	meatmentions(readfile(infile)) # Since something went wrong; Restart the entire process and choose a completely new tweet

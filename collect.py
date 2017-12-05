"""
collect.py
"""
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
import pickle
import string
from TwitterAPI import TwitterAPI



consumer_key = 'kBvjgHEEyqDEAkwolXXdwzQAc'
consumer_secret = '2YJjfIhdFAm7II5bg5f3Uj18vRCM31N8b9c4sBZYspqFSFiNgD'
access_token = '771960687681822722-s5ox0ZYRqo1YIUdjEfwxtg3r9Qr5mzI'
access_token_secret = 'e18Nnxm89VlHKc9M5gaquzmFdsjnhsgMeXCbxeEyLSGn9'


def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

def robust_request(twitter, resource, params, max_tries=5):
	""" If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
	"""
	for i in range(max_tries):
		request = twitter.request(resource, params)
		if request.status_code == 200:
			return request
		elif request.status_code == 404 or request.status_code == 403:
			print("error!!!!")
			return -1
		else:
			print('Got error %s \nsleeping for 15 minutes.' % request.text)
			sys.stderr.flush()
			time.sleep(61 * 15)

def get_tweets(request):
	"""
	this method collects tweetsand appends it into a list.
	:param request:
	:return:
	"""
	count = 0
	limit = 2000
	tweets = []
	for i in request:
		if 'user' in i:
			count+=1
			tweets.append(i)
		if(count%100 == 0):
			print("%d tweets collected" %count)
		if(count>limit):
			return tweets
			
def get_screen_names():
	screen_names = []
	tweets = pickle.load( open( 'tweets.pkl', 'rb' ) )
	count = 0
	for i in tweets:
		count+=1
		screen_names.append(i['user']['screen_name'])
		if count>150:
			return screen_names

def get_followed(screen_name,twitter):
	""" Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids
    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.
    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.
    Note: If a user follows more than 5000 accounts, we will limit ourselves to
    the first 5000 accounts returned.
    In this test case, I return the first 5 accounts that I follow.
    >>> twitter = get_twitter()
    >>> get_friends(twitter, 'aronwc')[:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
	"""
	print ('fetching friends for '+screen_name)
	followed = []
	request = robust_request(twitter,'friends/list',{'screen_name' : screen_name,'count': 200}) #create the request for friend's list
	if request!=-1:
		f = [i for i in request] # iterate through each response to get candidate's friends' details
		for i in range(len(f)):
			followed.append(f[i]['screen_name'])
		return followed
	else:
		return followed

def all_followed(screen_names,twitter):
    """ Get the friends for all the users in usernames.
    I.e., call get_friends for all 15 candidates.
    Args:
        screen_names: a list of Twitter screen names, one per candidate
    Returns:
        a dict mapping each candidate's username (string) to a list of his/her friends (strings)
    """
    return {i: get_followed(i,twitter) for i in screen_names}

def count_friends(followed):
	""" Count how often each friend is followed.
	    Args:
	        users: a list of user dicts
	    Returns:
	        a Counter object mapping each friend to the number of candidates who follow them.
	        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter
	    In this example, friend '2' is followed by three different users.
	    >>> c = count_friends([{'friends': [1,2]}, {'friends': [2,3]}, {'friends': [2,3]}])
	    >>> c.most_common()
	    [(2, 3), (3, 2), (1, 1)]
	"""
	count=Counter()
	for i in  followed.values():
		count.update(i)
	return count
    	
def main():	
			
	twitter = get_twitter()
	#for new york or sanfransisco location, got this from https://dev.twitter.com/streaming/overview/request-parameters#locations
	request = robust_request(twitter, 'statuses/filter', {'locations':'-122.75,36.8,-121.75,37.8,-74,40,-73,41','track':'trump,hilary,election','lang':'en'})
	print("data collection started!!")
	print("This might take a few minutes please be patient!!")
	tweets = get_tweets(request)
	pickle.dump(tweets, open('tweets.pkl','wb'))
	print("tweets collected successfully!!")
	screen_names = get_screen_names()
	print('Screennames collected successfully!!')
	screen_names = set(screen_names)
	screen_names = list(screen_names)
	screen_names = screen_names[:14]
	print("collecting friends for each user!! this might take time. You can run classify till then!!")
	followed = all_followed(screen_names, twitter)
	followed_total = count_friends(followed)
	pickle.dump(followed, open('followed.pkl','wb'))
	pickle.dump(followed_total, open('followed_total.pkl','wb'))
	print("Data Collected Successfully!!!")
	
if __name__ == '__main__':
    main()	








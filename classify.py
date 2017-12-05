"""
classify.py
"""
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
import pickle
import string
import re
import requests
#from pprint import pprint

def get_census_names():
    """ Fetch a list of common male/female names from the census.
    For ambiguous names, we select the more frequent gender."""
    males = requests.get('http://www2.census.gov/topics/genealogy/1990surnames/dist.male.first').text.split('\n')
    females = requests.get('http://www2.census.gov/topics/genealogy/1990surnames/dist.female.first').text.split('\n')
    males_pct = dict([(m.split()[0].lower(), float(m.split()[1]))
                  for m in males if m])
    females_pct = dict([(f.split()[0].lower(), float(f.split()[1]))
                    for f in females if f])
    male_names = set([m for m in males_pct if m not in females_pct or
                  males_pct[m] > females_pct[m]])
    female_names = set([f for f in females_pct if f not in males_pct or
                  females_pct[f] > males_pct[f]])
    return male_names, female_names

def get_first_name(tweet):
    if 'user' in tweet and 'name' in tweet['user']:
        parts = tweet['user']['name'].split()
        if len(parts) > 0:
            return parts[0].lower()

def gender_by_name(tweets, male_names, female_names):
    male = []
    female = []
    unknown = []
    for t in tweets:
        name = t['user']['name']
        if name:
            # remove punctuation.
            name_parts = re.findall('\w+', name.split()[0].lower())
            if len(name_parts) > 0:
                first = name_parts[0].lower()
                if first in male_names:
                    t['gender'] = 'male'
                    male.append(first)
                elif first in female_names:
                    t['gender'] = 'female'
                    female.append(first)
                else:
                    t['gender'] = 'unknown'
                    unknown.append(first)
    return male,female,unknown,tweets

def main():
    print("Classification started")
    tweets = pickle.load(open('tweets.pkl', 'rb'))
    #name = []
    for i in tweets:
        #name.append(i['user']['name'])
        i['gender'] = 'unknown'
    male_names, female_names = get_census_names()
    male, female, unknown,tweets_gender = gender_by_name(tweets, male_names, female_names)
    pickle.dump(male, open('male.pkl', 'wb'))
    pickle.dump(female, open('female.pkl', 'wb'))
    pickle.dump(unknown, open('unknown.pkl', 'wb'))
    pickle.dump(tweets_gender, open('tweets_gender.pkl', 'wb'))
    print("classification completed successfully!!! Please run summarize.py")


if __name__ == '__main__':
    main()